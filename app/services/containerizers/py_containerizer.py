import importlib
import json
import sys
from abc import ABC

import distro

from app.models.workflow_cell import Cell
from app.services.containerizers.containerizer import Containerizer


class PyContainerizer(Containerizer, ABC):

    def __init__(self, cell: Cell):
        super().__init__(cell)
        self.file_extension = '.py'
        if self.visualization_cell:
            self.template_script = 'vis_cell_template.jinja2'
        else:
            self.template_script = 'R_cell_template.jinja2'

    def extract_notebook(self):
        return json.dumps(self.cell.notebook_dict, indent=4)

    def is_standard_module(self, module_name=None):
        if module_name in sys.builtin_module_names:
            return True
        installation_path = None
        try:
            installation_path = importlib.import_module(module_name).__file__
        except ImportError:
            return False
        linux_os = distro.id()
        return 'dist-packages' not in installation_path \
            if linux_os == 'Ubuntu' else ('site-packages' not in
                                          installation_path)
