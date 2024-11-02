import json
import logging
import os
import re
from typing import Literal, Union

import jsonschema
import yaml

from .extractor import Extractor
from ...models.notebook_data import NotebookData


class HeaderExtractor(Extractor):
    """ Extracts cells using information defined by the user in its header

    Cells should contain a comment with a yaml block defining inputs, outputs,
    params, secrets and confs. Eg:

    # My cell
    # ---
    # NaaVRE:
    #   cell:
    #     inputs:
    #       - my_input:
    #           type: String
    #       - my_other_input:
    #           type: Integer
    #     outputs:
    #       - my_output:
    #           type: List
    #     params:
    #       - param_something:
    #           type: String
    #           default_value: "my default value"
    #     secrets:
    #       - secret_api_key:
    #           type: String
    #     confs:
    #       - conf_something_else:
    #           assignation: "conf_something_else = 'my other value'"
    # ...
    [cell code]

    The document is validated with the schema `cell_header.schema.json`

    """

    def __init__(self, notebook_data: NotebookData):
        self.re_yaml_doc_in_comment = re.compile(
            (r"^(?:.*\n)*"
             r"\s*#\s*---\s*\n"
             r"((?:\s*#.*\n)+?)"
             r"\s*#\s*\.\.\.\s*\n"
             ),
            re.MULTILINE)
        cell_source = notebook_data.notebook.cells[
            notebook_data.cell_index].source
        self.schema = self._load_schema()
        self.cell_header = self._extract_header(cell_source)
        self._external_extract_cell_params = None
        self._external_extract_cell_secrets = None

        super().__init__(notebook_data)

    @staticmethod
    def _load_schema():
        filename = os.path.join(
            os.path.dirname(__file__),
            'cell_header.schema.json')
        with open(filename) as f:
            schema = json.load(f)
        return schema

    def enabled(self):
        return self.cell_header is not None

    def is_complete(self):
        return (
                (self.cell_inputs is not None)
                and (self.cell_outputs is not None)
                and (self.cell_params is not None)
                and (self.cell_secrets is not None)
                and (self.cell_confs is not None)
                and (self.cell_dependencies is not None)
        )

    def _extract_header(self, cell_source):
        # get yaml document from cell comments
        m = self.re_yaml_doc_in_comment.match(cell_source)
        if not (m and m.groups()):
            return None
        yaml_doc = m.group(1)
        # remove comment symbol
        yaml_doc = '\n'.join([
            line.lstrip().lstrip('#')
            for line in yaml_doc.splitlines()
        ])
        # parse yaml
        header = yaml.safe_load(yaml_doc)
        # validate schema
        try:
            jsonschema.validate(header, self.schema)
        except jsonschema.ValidationError as e:
            logging.getLogger().debug(f"Cell header validation error: {e}")
            raise e
        return header

    def add_missing_values(self, extractor: Extractor):
        """ Add values not specified in the header from another extractor
        (e.g. PyExtractor or RExtractor)
        """
        if self.cell_inputs is None:
            self.cell_inputs = extractor.infer_cell_inputs()
        if self.cell_outputs is None:
            self.cell_outputs = extractor.infer_cell_outputs()
        if self.cell_params is None:
            self.cell_params = extractor.extract_cell_params()
            # We store a reference to extractor.extract_cell_params because
            # self.extract_cell_params is called after self.add_missing_values
            # in component_containerizer.handlers.ExtractorHandler.post()
            self._external_extract_cell_params = extractor.extract_cell_params
        if self.cell_secrets is None:
            self.cell_secrets = extractor.cell_secrets
            # Same as self._external_extract_cell_params
            self._external_extract_cell_secrets = (
                extractor.extract_cell_secrets())
        if self.cell_confs is None:
            self.cell_confs = extractor.extract_cell_conf_ref()
        if self.cell_dependencies is None:
            self.cell_dependencies = (
                extractor.infer_cell_dependencies(self.cell_confs))

    @staticmethod
    def _parse_interface_vars_items(
            item: Union[str, dict],
            item_type: Literal['inputs', 'outputs', 'params', 'secrets'],
    ) -> dict:
        """ Parse interface variables (inputs, outputs, params, secrets) items

        They can have either format
        - ElementVarName: 'my_name'
        - ElementVarNameType {'my_name': 'my_type'}
        - IOElementVarDict {'my_name': {'type': 'my_type'}}
          or ParamElementVarDict {'my_name': {'type': 'my_type',
                                              'default_value': 'my_value'}}
          or SecretElementVarDict {'my_name': {'type': 'my_type'}}

        Returns
        - if item_type is 'inputs', 'outputs' or 'secrets':
            {'name': 'my_name', 'type': 'my_type'}
        - if item_type is 'params':
            {'name': 'my_name', 'type': 'my_type', 'value': 'my_value'}
        """
        var_dict = {}

        # ElementVarName
        if isinstance(item, str):
            var_dict = {
                'name': item,
                'type': None,
                'value': None,
            }
        elif isinstance(item, dict):
            if len(item.keys()) != 1:
                # this should have been caught by the schema validation
                raise ValueError(f"Unexpected item in {item_type}: {item}")
            var_name = list(item.keys())[0]
            var_props = item[var_name]
            # ElementVarNameType
            if isinstance(var_props, str):
                var_dict = {
                    'name': var_name,
                    'type': var_props,
                    'value': None,
                }
            # IOElementVarDict or ParamElementVarDict
            elif isinstance(var_props, dict):
                var_dict = {
                    'name': var_name,
                    'type': var_props.get('type'),
                    'value': var_props.get('default_value'),
                }

        if (var_dict['type'] == 'List') and (var_dict['value'] is not None):
            var_dict['value'] = json.dumps(var_dict['value'])

        # Convert types
        types_conversion = {
            'Integer': 'int',
            'Float': 'float',
            'String': 'str',
            'List': 'list',
            None: None,
        }
        var_dict['type'] = types_conversion[var_dict['type']]

        # 'value' should only be kept for params
        if item_type not in ['params']:
            del var_dict['value']

        return var_dict

    def _infer_cell_interface_vars(
            self,
            header: Union[dict, None],
            item_type: Literal['inputs', 'outputs', 'params', 'secrets'],
    ) -> Union[dict, None]:
        if header is None:
            return None
        items = header['NaaVRE']['cell'].get(item_type)
        if items is None:
            return None
        items = [self._parse_interface_vars_items(it, item_type)
                 for it in items]
        return {it['name']: it for it in items}

    def infer_cell_inputs(self):
        return self._infer_cell_interface_vars(
            self.cell_header,
            'inputs',
        )

    def infer_cell_outputs(self):
        return self._infer_cell_interface_vars(
            self.cell_header,
            'outputs',
        )

    def extract_cell_params(self):
        if self._external_extract_cell_params is not None:
            return self._external_extract_cell_params(self.cell_source)
        return self._infer_cell_interface_vars(
            self._extract_header(self.cell_source),
            'params',
        )

    def extract_cell_secrets(self):
        if self._external_extract_cell_secrets is not None:
            return self._external_extract_cell_secrets(self.cell_source)
        return self._infer_cell_interface_vars(
            self._extract_header(self.cell_source),
            'secrets',
        )

    def extract_cell_conf_ref(self):
        if self.cell_header is None:
            return None
        items = self.cell_header['NaaVRE']['cell'].get('confs')
        if items is None:
            return None
        return {k: v['assignation'] for it in items for k, v in it.items()}

    def infer_cell_dependencies(self, confs):
        if self.cell_header is None:
            return None
        items = self.cell_header['NaaVRE']['cell'].get('dependencies')
        if items is None:
            return None
        return [
            {
                'name': it.get('name'),
                'asname': it.get('asname', None),
                'module': it.get('module', ''),
            }
            for it in items]
