from abc import abstractmethod, ABC

from app.models.cell import Cell
from jinja2 import Environment, PackageLoader

class Containerizer():

    def __init__(self,cell: Cell):
        self.cell = cell
        self.check_has_type()
        self.check_has_base_image()
        loader = PackageLoader('app', 'templates')
        self.template_env = Environment(loader=loader, trim_blocks=True, lstrip_blocks=True)


    def check_has_type(self):
        all_vars = self.cell.params + self.cell.inputs + self.cell.outputs
        for parm_name in all_vars:
            if parm_name not in self.cell.types:
                raise ValueError(parm_name + ' has not type')
        pass

    def check_has_base_image(self):
        if self.cell.base_image is None:
            raise ValueError('base_image is not set')
        pass

    def containerize(self):
        template_cell = self.build_template_cell()
        return self.cell

    @abstractmethod
    def build_template_cell(self):
        pass

    @abstractmethod
    def build_visualization_template_cell(self):
        pass

    @abstractmethod
    def extract_notebook(self):
        pass

