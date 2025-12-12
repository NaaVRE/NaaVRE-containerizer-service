import inspect


from app.models.notebook_data import NotebookData

# Utility class to run sanity checks on NotebookData
# add more checks as methods named `check_<something>`


class NotebookSanityChecks:

    def __init__(self, notebook_data: NotebookData):
        self.notebook_data = notebook_data

    def run_all(self):
        """
        Call all instance methods named `check_<something>`
        Methods are run in deterministic order (sorted by name).
        """
        for name, method in sorted(
                inspect.getmembers(self, predicate=inspect.ismethod)):
            if name.startswith('check_'):
                method()
