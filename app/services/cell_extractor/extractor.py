import abc
import hashlib
import json

from slugify import slugify

from app.models.notebook_data import NotebookData
from app.models.workflow_cell import Cell
from app.services.converter.converter import ConverterReactFlowChart


class Extractor(abc.ABC):
    cell_inputs: list
    cell_outputs: list
    cell_params: list
    cell_secrets: list
    cell_confs: list
    cell_dependencies: list

    def __init__(self, notebook_data: NotebookData):
        self.notebook = notebook_data.notebook
        self.cell_source = (
            notebook_data.notebook.cells[notebook_data.cell_index].source)

        self.cell_inputs = self.infer_cell_inputs()
        self.cell_outputs = self.infer_cell_outputs()
        self.cell_params = self.extract_cell_params()
        self.cell_secrets = self.extract_cell_secrets()
        self.cell_confs = self.extract_cell_conf_ref()
        self.cell_dependencies = self.infer_cell_dependencies(self.cell_confs)
        self.user_name = notebook_data.user_name

    def extract_cell(self) -> Cell:
        title = self.cell_source.partition('\n')[0].strip()
        title = slugify(title) if title and title[0] == "#" else "Untitled"
        title += '-' + slugify(self.user_name)
        cell_identity_dict = {
            'title': title,
            'params': self.cell_params,
            'secrets': self.cell_secrets,
            'inputs': self.cell_inputs,
            'outputs': self.cell_outputs,
        }
        cell_identity_str = json.dumps(cell_identity_dict, sort_keys=True)
        node_id = hashlib.sha1(cell_identity_str.encode()).hexdigest()[:7]
        node = ConverterReactFlowChart.get_node(
            node_id,
            title,
            self.cell_inputs,
            self.cell_outputs,
            self.cell_params,
            self.cell_secrets,
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
        cell_dict = {
            'title': title,
            'params': self.cell_params,
            'secrets': self.cell_secrets,
            'inputs': self.cell_inputs,
            'outputs': self.cell_outputs,
            'confs': self.cell_confs,
            'dependencies': self.cell_dependencies,
            'base_container_image': None,
            'chart_obj': chart,
        }
        return Cell.model_validate(cell_dict)

    @abc.abstractmethod
    def infer_cell_inputs(self) -> list[dict]:
        pass

    @abc.abstractmethod
    def infer_cell_outputs(self) -> list[dict]:
        pass

    @abc.abstractmethod
    def extract_cell_params(self) -> list[dict]:
        pass

    @abc.abstractmethod
    def extract_cell_secrets(self) -> list[dict]:
        pass

    @abc.abstractmethod
    def extract_cell_conf_ref(self):
        pass

    @abc.abstractmethod
    def infer_cell_dependencies(self, confs) -> list[dict]:
        pass


class DummyExtractor(Extractor):
    def infer_cell_inputs(self):
        return {}

    def infer_cell_outputs(self):
        return {}

    def extract_cell_params(self):
        return {}

    def extract_cell_secrets(self):
        return {}

    def extract_cell_conf_ref(self):
        return []

    def infer_cell_dependencies(self, confs):
        return []
