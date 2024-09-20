from abc import ABC
from os import readv

from app.models.cell import Cell
from app.services.containerizers.containerizer import Containerizer


class RContainerizer(Containerizer, ABC):

    def __init__(self, cell: Cell):
        super().__init__(cell)

    def build_template_cell(self):
        raise NotImplementedError

    def build_visualization_template_cell(self):
        raise NotImplementedError