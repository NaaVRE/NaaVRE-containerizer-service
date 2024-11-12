import logging
from typing import Literal, Optional

from pydantic import BaseModel

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class Cell(BaseModel):
    title: str
    base_container_image: dict
    inputs: Optional[list[dict]] | None = None
    outputs: Optional[list[dict]] | None = None
    params: Optional[list[dict]] | None = None
    secrets: Optional[list[dict]] | None = None
    confs: Optional[list[dict]] | None = None
    dependencies: Optional[list[dict]] | None = None
    chart_obj: dict | None = None
    kernel: Literal['python', 'IRkernel', 'ipython', 'c']
    original_source: str
    image_version: str | None = None

    def __init__(self, **data):
        super().__init__(**data)
        # if self.title:
        #     self.title = slugify(self.title.strip())
        # if self.inputs:
        #     self.add_inputs(self.inputs)
        # if self.outputs:
        #     self.add_outputs(self.outputs)
        # if self.params:
        #     self.add_params(self.params)
        # if self.secrets:
        #     self.secrets = self.secrets or []
        #     self.add_secrets(self.secrets)
        # if self.dependencies and any(self.dependencies):
        #     self.dependencies = list(
        #         sorted(self.dependencies, key=lambda x: x['name']))

    # def _extract_types(self, vars_dict):
    #     """ Extract types to self.types and return list of var names
    #
    #     :param vars_dict: {'var1': {'name: 'var1', 'type': 'str'},
    #     'var2': ...}
    #     :return: ['var1', 'var2', ...]
    #     """
    #     names = []
    #     for var_props in vars_dict.values():
    #         var_type = var_props['type']
    #         var_name = var_props['name']
    #         self.types[var_name] = var_type
    #         names.append(var_name)
    #     return names
    #
    # def generate_dependencies(self):
    #     resolves = []
    #     for d in self.dependencies:
    #         resolve_to = "import %s" % d['name']
    #         if d['module']:
    #             resolve_to = "from %s %s" % (d['module'], resolve_to)
    #         if d['asname']:
    #             resolve_to += " as %s" % d['asname']
    #         resolves.append(resolve_to)
    #     return resolves
    #
    # def generate_configuration(self):
    #     resolves = []
    #     for c in self.confs:
    #         resolves.append(self.confs[c])
    #     return resolves
    #
    # def generate_configuration_dict(self):
    #     resolves = []
    #     assignment_symbol = '='
    #     for c in self.confs:
    #         if '=' in self.confs[c]:
    #             assignment_symbol = '='
    #         elif '<-' in self.confs[c]:
    #             assignment_symbol = '<-'
    #         assignment = self.confs[c].split(assignment_symbol)[1].replace(
    #             assignment_symbol, '').strip()
    #         conf = {c: assignment}
    #         resolves.append(conf)
    #     return resolves
