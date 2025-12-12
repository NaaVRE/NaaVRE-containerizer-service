import inspect
import re

from app.models.workflow_cell import Cell


# Utility class to run sanity checks on NotebookData
# add more checks as methods named `check_<something>`

class CellSanityChecks:

    def __init__(self, cell: Cell):
        self.cell = cell

    def run_all(self):
        """
        Call all instance methods named `check_<something>` with `cell`.
        Methods are run in deterministic order (sorted by name).
        """
        for name, method in sorted(
                inspect.getmembers(self, predicate=inspect.ismethod)):
            if name.startswith('check_'):
                method()

    def check_title(self):
        """
        Example check: ensure notebook title does not start with a digit.
        """
        title = self.cell.title
        pattern = re.compile(r'^\d')
        if pattern.match(title):
            raise ValueError("Cell title is: '" + title +
                             "'. It should not start with a digit.")
