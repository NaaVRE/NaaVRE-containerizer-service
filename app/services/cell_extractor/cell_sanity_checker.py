import re
from abc import ABC

from app.models.workflow_cell import Cell
from app.utils.sanity_checker import SanityChecker


class CellSanityChecker(SanityChecker, ABC):

    def __init__(self, cell: Cell):
        self.cell = cell

    def check_title(self):
        """
        Example check: ensure notebook title does not start with a digit.
        """
        title = self.cell.title
        pattern = re.compile(r'^\d')
        if pattern.match(title):
            raise ValueError("Cell title is: '" + title +
                             "'. It should not start with a digit.")
