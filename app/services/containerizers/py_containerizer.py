import json
from abc import ABC
import autopep8
from app.models.cell import Cell
from app.services.containerizers.containerizer import Containerizer


class PyContainerizer(Containerizer, ABC):

    def __init__(self, cell: Cell):
        super().__init__(cell)

    def build_template_cell(self):
        template_cell = self.template_env.get_template('py_cell_template.jinja2')
        compiled_code = template_cell.render(cell=self.cell, deps=self.cell.generate_dependencies(), types=self.cell.types,
                                             confs=self.cell.generate_configuration_dict())
        compiled_code = autopep8.fix_code(compiled_code)
        self.cell.container_source = compiled_code
        return template_cell.render(cell=self.cell, deps=self.cell.generate_dependencies(), types=self.cell.types,
                             confs=self.cell.generate_configuration_dict())

    def build_visualization_template_cell(self):
        template_cell = self.template_env.get_template('vis_cell_template.jinja2')
        compiled_code = template_cell.render(cell=self.cell, deps=self.cell.generate_dependencies(), types=self.cell.types,
                                             confs=self.cell.generate_configuration_dict())
        compiled_code = autopep8.fix_code(compiled_code)
        self.cell.container_source = compiled_code
        return template_cell.render(cell=self.cell, deps=self.cell.generate_dependencies(), types=self.cell.types,
                             confs=self.cell.generate_configuration_dict())

    def extract_notebook(self):
        return json.dumps(self.cell.notebook_dict, indent=4)