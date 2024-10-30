from abc import ABC

from app.models.workflow_cell import Cell
from app.services.containerizers.containerizer import Containerizer


class RContainerizer(Containerizer, ABC):

    def __init__(self, cell: Cell):
        super().__init__(cell)
        self.file_extension = '.R'
        self.template_script = 'R_cell_template.jinja2'

    def build_visualization_template_cell(self):
        raise NotImplementedError
