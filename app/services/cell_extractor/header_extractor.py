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
    schema: dict
    re_yaml_doc_in_comment: re.Pattern
    cell_header: Union[dict, None]

    def __init__(self, notebook_data: NotebookData):
        self.re_yaml_doc_in_comment = re.compile(
            (r"^(?:.*\n)*"
             r"\s*#\s*---\s*\n"
             r"((?:\s*#.*\n)+?)"
             r"\s*#\s*\.\.\.\s*\n"
             ),
            re.MULTILINE)
        self.schema = self._load_schema()
        self.cell_source = (
            notebook_data.notebook.cells[notebook_data.cell_index].source)
        self.cell_header = self._extract_header()
        super().__init__(notebook_data)
        #
        # self._external_extract_cell_params = None
        # self._external_extract_cell_secrets = None

    @staticmethod
    def _load_schema() -> dict:
        filename = os.path.join(
            os.path.dirname(__file__),
            'cell_header.schema.json')
        with open(filename) as f:
            schema = json.load(f)
        return schema

    def is_complete(self):
        return (
                self.cell_inputs
                and self.cell_outputs
                and self.cell_params
                and self.cell_secrets
                and self.cell_confs
                and self.cell_dependencies
        )

    def _extract_header(self) -> Union[dict, None]:
        # get yaml document from cell comments
        m = self.re_yaml_doc_in_comment.match(self.cell_source)
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

    def mearge_values(self, extractor: Extractor):
        """ Add values not specified in the header from another extractor
        (e.g. PyExtractor or RExtractor)
        """
        if not self.cell_inputs:
            self.cell_inputs = extractor.cell_inputs
        else:
            for var in extractor.cell_inputs:
                if var not in self.cell_inputs:
                    self.cell_inputs.append(var)
        if not self.cell_outputs:
            self.cell_outputs = extractor.cell_outputs
        else:
            for var in extractor.cell_outputs:
                if var not in self.cell_outputs:
                    self.cell_outputs.append(var)
        if not self.cell_params:
            self.cell_params = extractor.cell_params
        else:
            for var in extractor.cell_params:
                if var not in self.cell_params:
                    self.cell_params.append(var)
        if not self.cell_secrets:
            self.cell_secrets = extractor.cell_secrets
        else:
            for var in extractor.cell_secrets:
                if var not in self.cell_secrets:
                    self.cell_secrets.append(var)
        if not self.cell_confs:
            self.cell_confs = extractor.cell_confs
        else:
            for var in extractor.cell_confs:
                if var not in self.cell_confs:
                    self.cell_confs.append(var)
        if not self.cell_dependencies:
            self.cell_dependencies = extractor.cell_dependencies
        else:
            for var in extractor.cell_dependencies:
                if var not in self.cell_dependencies:
                    self.cell_dependencies.append(var)

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
        elif item_type in ['params']:
            var_dict['default_value'] = var_dict['value']
            del var_dict['value']
        return var_dict

    def _infer_cell_interface_vars(
            self,
            header: Union[dict, None],
            item_type: Literal['inputs', 'outputs', 'params', 'secrets'],
    ) -> list[dict]:
        if header is None:
            return []
        vars = []
        items = header['NaaVRE']['cell'].get_base_image_tags(item_type)
        if items is None:
            return []
        for item in items:
            var = self._parse_interface_vars_items(item, item_type)
            vars.append(var)
        return vars

    def get_cell_inputs(self) -> list[dict]:
        inputs = self._infer_cell_interface_vars(
            self.cell_header,
            'inputs',
        )
        return inputs

    def get_cell_outputs(self) -> list[dict]:
        outputs = self._infer_cell_interface_vars(
            self.cell_header,
            'outputs',
        )
        return outputs

    def get_cell_params(self) -> list[dict]:
        params = self._infer_cell_interface_vars(
            self._extract_header(),
            'params',
        )
        return params

    def get_cell_secrets(self) -> list[dict]:
        secrets = self._infer_cell_interface_vars(
            self._extract_header(),
            'secrets',
        )
        return secrets

    def get_cell_confs(self) -> list[dict]:
        if self.cell_header is None:
            return []
        items = self.cell_header['NaaVRE']['cell'].get_base_image_tags('confs')
        if items is None:
            return []
        confs = []
        for item in items:
            for k, v in item.items():
                if 'assignation' in v:
                    assignation = v.get_base_image_tags('assignation')
                    if '[' in assignation and ']' in assignation:
                        # Replace to R list format
                        assignation = assignation.replace('[',
                                                          'list(').replace(']',
                                                                           ')')
                        item[k]['assignation'] = assignation
            confs.append({k: v['assignation'] for k, v in item.items()})
        return confs

    def get_cell_dependencies(self, confs) -> list[dict]:
        if self.cell_header is None:
            return []
        items = self.cell_header['NaaVRE']['cell'].get_base_image_tags(
            'dependencies')
        if items is None:
            return []
        return [
            {
                'name': it.get_base_image_tags('name'),
                'asname': it.get_base_image_tags('asname', None),
                'module': it.get_base_image_tags('module', ''),
            }
            for it in items]
