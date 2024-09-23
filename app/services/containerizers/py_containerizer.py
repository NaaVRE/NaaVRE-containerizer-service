from abc import ABC
import importlib
import json
import sys
from abc import ABC
import distro
import autopep8

from app.models.cell import Cell
from app.services.containerizers.containerizer import Containerizer, load_module_name_mapping


class PyContainerizer(Containerizer, ABC):

    def __init__(self, cell: Cell):
        super().__init__(cell)

    def build_template_cell(self):
        if self.visualization_cell:
            template = 'vis_cell_template.jinja2'
        else:
            template = 'py_cell_template.jinja2'
        template_cell = self.template_env.get_template(template)
        compiled_code = template_cell.render(cell=self.cell, deps=self.cell.generate_dependencies(), types=self.cell.types,
                                             confs=self.cell.generate_configuration_dict())
        compiled_code = autopep8.fix_code(compiled_code)
        self.cell.container_source = compiled_code
        return template_cell.render(cell=self.cell, deps=self.cell.generate_dependencies(), types=self.cell.types,
                             confs=self.cell.generate_configuration_dict())

    def extract_notebook(self):
        return json.dumps(self.cell.notebook_dict, indent=4)


    def is_standard_module(self,module_name=None):
        if module_name in sys.builtin_module_names:
            return True
        installation_path = None
        try:
            installation_path = importlib.import_module(module_name).__file__
        except ImportError:
            return False
        linux_os = distro.id()
        return 'dist-packages' not in installation_path if linux_os == 'Ubuntu' else 'site-packages' not in installation_path