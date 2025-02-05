from abc import ABC

from app.models.workflow_cell import Cell
from app.services.containerizers.containerizer import Containerizer


class JuliaContainerizer(Containerizer, ABC):

    def __init__(self, cell: Cell, module_mapping_url=None):
        super().__init__(cell, module_mapping_url)
        raise NotImplementedError

    def build_script(self):
        raise NotImplementedError

    def build_visualization_template_cell(self):
        raise NotImplementedError
