import abc
import copy
import hashlib
import json

from slugify import slugify

from app.models.notebook_data import NotebookData
from app.models.workflow_cell import Cell
from app.services.converter.converter import ConverterReactFlowChart


class Extractor(abc.ABC):
    inputs: list
    outputs: list
    params: list
    secrets: list
    confs: list
    dependencies: list

    def __init__(self, notebook_data: NotebookData):
        self.notebook_data = notebook_data
        self.notebook = notebook_data.notebook
        notebook_cells = self.notebook.cells
        self.cell_index = self.notebook_data.cell_index
        self.source = notebook_cells[self.cell_index].source
        self.kernel = self.notebook_data.kernel

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
        title += '-' + slugify(self.notebook_data.user_name)

        # If any of these change, we create a new cell in the catalog.
        # This matches the cell properties saved in workflows.
        cell_identity_dict = {
            'title': title,
            'params': self.params,
            'secrets': self.secrets,
            'inputs': self.inputs,
            'outputs': self.outputs,
        }
        cell_identity_str = json.dumps(cell_identity_dict, sort_keys=True)
        node_id = hashlib.sha1(cell_identity_str.encode()).hexdigest()[:7]
        # Create cell from dict
        cell = Cell(title=title,
                    task_name=slugify(title.lower()),
                    original_source=self.source,
                    inputs=self.inputs,
                    outputs=self.outputs,
                    params=self.params,
                    secrets=self.secrets,
                    confs=self.confs,
                    dependencies=self.dependencies,
                    container_source="",
                    kernel=self.kernel,
                    node_id=node_id
                    )
        node = ConverterReactFlowChart.get_node(
            node_id,
            title,
            self.inputs,
            self.outputs,
            self.params,
            self.secrets,
        )
        chart = {
            'offset': {
                'x': 0,
                'y': 0,
            },
            'scale': 1,
            'nodes': {node_id: node},
            'links': {},
            'selected': {},
            'hovered': {},
        }

        cell.chart_obj = chart
        return cell

    @abc.abstractmethod
    def get_cell_inputs(self):
        pass

    @abc.abstractmethod
    def get_cell_outputs(self):
        pass

    @abc.abstractmethod
    def get_cell_params(self):
        pass

    @abc.abstractmethod
    def get_cell_secrets(self):
        pass

    @abc.abstractmethod
    def extract_cell_conf_ref(self):
        pass

    @abc.abstractmethod
    def get_cell_dependencies(self):
        pass

    def _get_cell_by_index(self, notebook, cell_index):
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
    def get_cell_inputs(self):
        return {}

    def get_cell_outputs(self):
        return {}

    def get_cell_params(self):
        return {}

    def get_cell_secrets(self):
        return {}

    def extract_cell_conf_ref(self):
        return []

    def get_cell_dependencies(self):
        return []
