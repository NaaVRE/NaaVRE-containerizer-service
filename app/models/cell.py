import logging
import re
from typing import Literal, Optional

from pydantic import BaseModel
from slugify import slugify

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

class Cell(BaseModel):
    title: str | None = None
    task_name: str | None = None
    original_source: str | None = None
    base_image: dict
    inputs: Optional[list] | None = None
    outputs: Optional[list] | None = None
    params: Optional[list] | None = None
    param_values: Optional[dict] | None = None
    secrets: Optional[list] | None = None
    confs: Optional[dict] | None = None
    dependencies: Optional[list] | None = None
    chart_obj: dict | None = None
    node_id: str | None = None
    container_source: str | None = None
    global_conf: Optional[dict] | None = None
    kernel: Literal['python', 'IRkernel', 'ipython', 'c']
    notebook_dict: dict | None = None
    image_version: str | None = None
    types: Optional[dict] | None = None

    def __init__(self, **data):
        super().__init__(**data)
        self.title = slugify(self.title.strip())
        self.task_name = slugify(self.task_name)
        self.add_inputs(self.inputs)
        self.add_outputs(self.outputs)
        self.add_params(self.params)
        self.add_param_values(self.params)
        self.secrets = self.secrets or []
        self.add_secrets(self.secrets)
        # self.all_inputs = list(self.inputs) + list(self.params)
        self.dependencies = list(sorted(self.dependencies, key=lambda x: x['name']))

    def _extract_types(self, vars_dict):
        """ Extract types to self.types and return list of var names

        :param vars_dict: {'var1': {'name: 'var1', 'type': 'str'}, 'var2': ...}
        :return: ['var1', 'var2', ...]
        """
        names = []
        for var_props in vars_dict.values():
            var_type = var_props['type']
            var_name = var_props['name']
            self.types[var_name] = var_type
            names.append(var_name)
        return names

    def add_inputs(self, inputs):
        if isinstance(inputs, dict):
            inputs = self._extract_types(inputs)
        self.inputs = inputs

    def add_outputs(self, outputs):
        if isinstance(outputs, dict):
            outputs = self._extract_types(outputs)
        self.outputs = outputs

    def add_params(self, params):
        if isinstance(params, dict):
            params = self._extract_types(params)
        self.params = params

    def add_secrets(self, secrets):
        if isinstance(secrets, dict):
            secrets = self._extract_types(secrets)
        self.secrets = secrets

    def set_image_version(self, image_version):
        if not image_version:
            raise ValueError(
                "Image version cannot be empty. Cell title: %s" % self.title)
        self.image_version = image_version

    def add_param_values(self, params):
        self.param_values = {}
        if isinstance(params, dict):
            for param_props in params.values():
                if 'value' in param_props:
                    self.param_values[param_props['name']] = param_props[
                        'value']

    # def concatenate_all_inputs(self):
    #     self.all_inputs = list(self.inputs) + list(self.params)

    def clean_code(self):
        indices_to_remove = []
        lines = self.original_source.splitlines()
        self.original_source = ""
        for line_i in range(0, len(lines)):
            line = lines[line_i]
            # Do not remove line that startswith param_ if not in the self.params
            if line.startswith('param_'):
                # clean param name
                pattern = r"\b(param_\w+)\b"
                param_name = re.findall(pattern, line)[0]
                if param_name in self.params:
                    indices_to_remove.append(line_i)
            regex = r'^\s*(#|import|from)'
            if re.match(regex, line):
                indices_to_remove.append(line_i)

        for ir in sorted(indices_to_remove, reverse=True):
            lines.pop(ir)

        self.original_source = "\n".join(lines)

    def clean_task_name(self):
        self.task_name = slugify(self.task_name)

    def clean_title(self):
        self.title = slugify(self.title)
    #
    # def integrate_configuration(self):
    #     lines = self.original_source.splitlines()
    #     self.original_source = ""
    #     for idx, conf in enumerate(self.generate_configuration()):
    #         lines.insert(idx, conf)
    #     self.original_source = "\n".join(lines)
    #
    def generate_dependencies(self):
        resolves = []
        for d in self.dependencies:
            resolve_to = "import %s" % d['name']
            if d['module']:
                resolve_to = "from %s %s" % (d['module'], resolve_to)
            if d['asname']:
                resolve_to += " as %s" % d['asname']
            resolves.append(resolve_to)
        return resolves

    def generate_configuration(self):
        resolves = []
        for c in self.confs:
            resolves.append(self.confs[c])
        return resolves

    def generate_configuration_dict(self):
        resolves = []
        assignment_symbol = '='
        for c in self.confs:
            if '=' in self.confs[c]:
                assignment_symbol = '='
            elif '<-' in self.confs[c]:
                assignment_symbol = '<-'
            assignment = self.confs[c].split(assignment_symbol)[1].replace(assignment_symbol, '').strip()
            conf = {c: assignment}
            resolves.append(conf)
        return resolves
