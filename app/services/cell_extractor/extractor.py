import abc

from app.models.notebook_data import NotebookData
from app.services.cell_extractor.py_extractor import PyExtractor
from app.services.cell_extractor.py_header_extractor import PyHeaderExtractor
from app.services.cell_extractor.r_extractor import RExtractor
from app.services.cell_extractor.r_header_extractor import RHeaderExtractor


class Extractor(abc.ABC):
    ins: dict
    outs: dict
    params: dict
    secrets: dict
    confs: list
    dependencies: list

    def __init__(self, notebook, cell_source):
        self.notebook = notebook
        self.cell_source = cell_source

        self.ins = self.infer_cell_inputs()
        self.outs = self.infer_cell_outputs()
        self.params = self.extract_cell_params(cell_source)
        self.secrets = self.extract_cell_secrets(cell_source)
        self.confs = self.extract_cell_conf_ref()
        self.dependencies = self.infer_cell_dependencies(self.confs)

    def extract_cell(self, notebook_data: NotebookData):
        notebook = notebook_data.notebook
        cells = notebook.cells
        cell_index = notebook_data.cell_index
        source = cells[cell_index].source
        if notebook.cells[cell_index].cell_type != 'code':
            # dummy extractor for non-code cells (e.g. markdown)
            extractor = DummyExtractor(notebook, source)
        else:
            extractor = self._get_extractor(notebook, source,
                                            notebook_data.kernel)
        extractor.extract_cell_params(source)
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

    def _get_extractor(self, notebook, source, kernel):
        extractor = None
        if 'python' in kernel.lower():
            extractor = PyHeaderExtractor(notebook, source)
        elif 'r' in kernel.lower():
            extractor = RHeaderExtractor(notebook, source)
        if not extractor.is_complete():
            if kernel == "IRkernel":
                code_extractor = RExtractor(notebook, source)
            else:
                code_extractor = PyExtractor(notebook, source)
            extractor.add_missing_values(code_extractor)
        pass


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
