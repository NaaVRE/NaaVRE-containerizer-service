import json

from pydantic import BaseModel
import json
import logging
import re
from typing import Literal
from typing import Optional
from slugify import slugify

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

class Cell(BaseModel):
    title: str | None = None
    task_name: str | None = None
    original_source: str | None = None
    base_image: dict| None = None
    inputs: Optional[list]| None = None
    outputs: Optional[list]| None = None
    params: Optional[list]| None = None
    param_values: Optional[dict]| None = None
    secrets: Optional[list]| None = None
    confs: Optional[dict]| None = None
    dependencies: Optional[list]| None = None
    chart_obj: dict| None = None
    node_id: str| None = None
    container_source: str| None = None
    global_conf: Optional[dict]| None = None
    kernel: Literal ['python', 'r', 'ipython', 'c']
    notebook_json: dict| None = None
    image_version: str| None = None
    types: Optional[dict]| None = None

    def __init__(self, **data):
        super().__init__(**data)

    # def __init__(
    #         self,
    #         title,
    #         task_name,
    #         original_source,
    #         inputs,
    #         outputs,
    #         params,
    #         secrets,
    #         confs,
    #         dependencies,
    #         container_source,
    #         chart_obj=None,
    #         node_id='',
    #         kernel='',
    #         notebook_dict=None,
    #         image_version=None,
    #         base_image = None
    # ) -> None:
    #
    #     self.title = slugify(title.strip())
    #     self.task_name = slugify(task_name)
    #     self.original_source = original_source
    #     self.types = dict()
    #     self.add_inputs(inputs)
    #     self.add_outputs(outputs)
    #     self.add_params(params)
    #     self.add_param_values(params)
    #     self.add_secrets(secrets)
    #     self.confs = confs
    #     self.all_inputs = list(inputs) + list(params)
    #     self.dependencies = list(sorted(dependencies, key=lambda x: x['name']))
    #     self.chart_obj = chart_obj
    #     self.node_id = node_id
    #     self.container_source = container_source
    #     self.kernel = kernel
    #     self.notebook_dict = notebook_dict

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
            raise ValueError("Image version cannot be empty. Cell title: %s" % self.title)
        self.image_version = image_version

    def add_param_values(self, params):
        self.param_values = {}
        if isinstance(params, dict):
            for param_props in params.values():
                if 'value' in param_props:
                    self.param_values[param_props['name']] = param_props['value']

    def concatenate_all_inputs(self):
        self.all_inputs = list(self.inputs) + list(self.params)

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
            if re.match('^\s*(#|import|from)', line):
                indices_to_remove.append(line_i)

        for ir in sorted(indices_to_remove, reverse=True):
            lines.pop(ir)

        self.original_source = "\n".join(lines)

    def clean_task_name(self):
        self.task_name = slugify(self.task_name)

    def clean_title(self):
        self.title = slugify(self.title)

    def integrate_configuration(self):
        lines = self.original_source.splitlines()
        self.original_source = ""
        for idx, conf in enumerate(self.generate_configuration()):
            lines.insert(idx, conf)
        self.original_source = "\n".join(lines)

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
        for c in self.confs:
            assignment = self.confs[c].split('=')[1].replace('=', '').strip()
            conf = {c: assignment}
            resolves.append(conf)
        return resolves

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)