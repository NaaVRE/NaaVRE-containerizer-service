from abc import ABC

from app.models.cell import Cell
from app.services.containerizers.containerizer import Containerizer


class CContainerizer(Containerizer, ABC):

    def __init__(self, cell: Cell):
        super().__init__(cell)
        raise NotImplementedError

    def build_script(self):
        raise NotImplementedError

    def build_visualization_template_cell(self):
        raise NotImplementedError
