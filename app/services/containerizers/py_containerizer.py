import importlib
import json
import sys
from abc import ABC

import distro
import nbformat as nbf

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
        # Build a notebook from the cell
        nb = nbf.v4.new_notebook()
        cells = [nbf.v4.new_code_cell(self.cell.original_source)]
        nb.cells.extend(cells)
        return json.dumps(nb, indent=2)

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

    def map_dependencies(self, dependencies=None, module_name_mapping=None):
        conda_deps = set()
        pip_deps = set()
        for dep in dependencies:
            module_name = dep.get('module', dep.get('name'))
            if not module_name:
                continue
            module_name = module_name.split('.')[
                0] if '.' in module_name else module_name
            if module_name in module_name_mapping['conda']:
                conda_deps.add(module_name_mapping['conda'][module_name])
            elif module_name in module_name_mapping['pip']:
                pip_deps.add(module_name_mapping['pip'][module_name])
            elif not self.is_standard_module(module_name):
                conda_deps.add(module_name)
        return {'conda_dependencies': conda_deps, 'pip_dependencies': pip_deps}
