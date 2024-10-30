import abc
import copy
import json

from slugify import slugify

from app.models.notebook_data import NotebookData


class Extractor(abc.ABC):
    ins: dict
    outs: dict
    params: dict
    secrets: dict
    confs: list
    dependencies: list

    def __init__(self, notebook_data: NotebookData):
        self.user_name = None
        self.notebook_data = notebook_data
        self.notebook = notebook_data.notebook
        cells = self.notebook.cells
        self.cell_index = self.notebook_data.cell_index
        self.source = cells[self.cell_index].source
        self.kernel = self.notebook_data.kernel

        self.ins = self.infer_cell_inputs()
        self.outs = self.infer_cell_outputs()
        self.params = self.extract_cell_params(self.source)
        self.secrets = self.extract_cell_secrets(self.source)
        self.confs = self.extract_cell_conf_ref()
        self.dependencies = self.infer_cell_dependencies(self.confs)

        self.params = self.extract_cell_params(self.source)
        self.secrets = self.extract_cell_secrets(self.source)
        self.confs = self.extract_cell_conf_ref()
        self.dependencies = self.infer_cell_dependencies(self.confs)

    def set_user_name(self, user_name: str):
        self.user_name = user_name

    def extract_cell(self):
        # extracted_nb = self._extract_cell_by_index(self.notebook,
        #                                                     self.cell_index)
        # if self.kernel.lower() == "irkernel":
        #     extracted_nb = self._set_notebook_kernel(extracted_nb, 'R')
        # elif self.kernel.lower() == "ipython" or self.kernel.lower()
        #                                                          == "python":
        #     extracted_nb = self._set_notebook_kernel(extracted_nb, 'python3')
        # else:
        #     raise ValueError("Unsupported kernel")

        # initialize variables
        title = self.source.partition('\n')[0].strip()
        title = slugify(title) if title and title[0] == "#" else "Untitled"
        title += '-' + slugify(self.user_name)

        # If any of these change, we create a new cell in the catalog.
        # This matches the cell properties saved in workflows.
        cell_identity_dict = {
            'title': title,
            'params': self.params,
            'secrets': self.secrets,
            'inputs': self.ins,
            'outputs': self.outs,
        }
        cell_identity_str = json.dumps(cell_identity_dict, sort_keys=True)
        print(cell_identity_str)
        return {}

    @abc.abstractmethod
    def infer_cell_inputs(self):
        pass

    @abc.abstractmethod
    def infer_cell_outputs(self):
        pass

    @abc.abstractmethod
    def extract_cell_params(self, source):
        pass

    @abc.abstractmethod
    def extract_cell_secrets(self, source):
        pass

    @abc.abstractmethod
    def extract_cell_conf_ref(self):
        pass

    @abc.abstractmethod
    def infer_cell_dependencies(self, confs):
        pass

    def _extract_cell_by_index(self, notebook, cell_index):
        new_nb = copy.deepcopy(notebook)
        if cell_index < len(notebook.cells):
            new_nb.cells = [notebook.cells[cell_index]]
            return new_nb

    # Not sure why we need this method
    def _set_notebook_kernel(self, notebook, kernel):
        # new_nb = copy.deepcopy(notebook)
        # # Replace kernel name in the notebook metadata
        # new_nb.metadata.kernelspec.name = kernel
        # new_nb.metadata.kernelspec.display_name = kernel
        # new_nb.metadata.kernelspec.language = kernel
        # return new_nb
        return notebook


class DummyExtractor(Extractor):
    def infer_cell_inputs(self):
        return {}

    def infer_cell_outputs(self):
        return {}

    def extract_cell_params(self, source):
        return {}

    def extract_cell_secrets(self, source):
        return {}

    def extract_cell_conf_ref(self):
        return []

    def infer_cell_dependencies(self, confs):
        return []
