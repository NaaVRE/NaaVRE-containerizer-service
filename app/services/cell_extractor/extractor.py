import abc
import copy

from app.models.extractor_payload import ExtractorPayload


class Extractor(abc.ABC):
    # ins: dict
    # outs: dict
    # params: dict
    # secrets: dict
    # confs: list
    # dependencies: list

    # def __init__(self, notebook, cell_source):
    #     self.notebook = notebook
    #     self.cell_source = cell_source
    #
    #     self.ins = self.infer_cell_inputs()
    #     self.outs = self.infer_cell_outputs()
    #     self.params = self.extract_cell_params(cell_source)
    #     self.secrets = self.extract_cell_secrets(cell_source)
    #     self.confs = self.extract_cell_conf_ref()
    #     self.dependencies = self.infer_cell_dependencies(self.confs)

    def __init__(self, extractor_payload: ExtractorPayload):
        self.extractor_payload = extractor_payload

    def extract_cell(self):
        notebook_data = self.extractor_payload.data
        notebook = notebook_data.notebook
        cells = notebook.cells
        cell_index = notebook_data.cell_index
        kernel = notebook_data.kernel
        source = cells[cell_index].source

        print(kernel)
        print(source)

        # extracted_nb = self._extract_cell_by_index(notebook, cell_index)
        # if kernel.lower() == "irkernel":
        #     extracted_nb = self._set_notebook_kernel(extracted_nb, 'R')
        # else:
        #     extracted_nb = self._set_notebook_kernel(extracted_nb, 'python3')
        #
        # # initialize variables
        # title = source.partition('\n')[0].strip()
        # title = slugify(title) if title and title[0] == "#" else "Untitled"
        #
        # if 'JUPYTERHUB_USER' in os.environ:
        #     title += '-' + slugify(os.environ['JUPYTERHUB_USER'])

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

    def _set_notebook_kernel(self, notebook, kernel):
        new_nb = copy.deepcopy(notebook)
        # Replace kernel name in the notebook metadata
        new_nb.metadata.kernelspec.name = kernel
        new_nb.metadata.kernelspec.display_name = kernel
        new_nb.metadata.kernelspec.language = kernel
        return new_nb


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
