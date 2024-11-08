import abc
import hashlib
import json

from slugify import slugify

from app.models.notebook_data import NotebookData
from app.models.workflow_cell import Cell
from app.services.base_image_tags import BaseImageTags
from app.services.converter.converter import ConverterReactFlowChart


class Extractor(abc.ABC):
    user_name: str
    cell_source: str
    cell_inputs: list
    cell_outputs: list
    cell_params: list
    cell_secrets: list
    cell_confs: list
    cell_dependencies: list
    kernel: str

    def __init__(self, notebook_data: NotebookData):
        self.cell_source = (
            notebook_data.notebook.cells[notebook_data.cell_index].source)
        self.user_name = notebook_data.user_name
        self.kernel = notebook_data.kernel
        self.cell_inputs = self.get_cell_inputs()
        self.cell_outputs = self.get_cell_outputs()
        self.cell_params = self.get_cell_params()
        self.cell_secrets = self.get_cell_secrets()
        self.cell_confs = self.get_cell_confs()
        self.cell_dependencies = self.get_cell_dependencies(self.cell_confs)
        self.base_image_name = notebook_data.base_image_name

    def get_cell(self) -> Cell:
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
        base_image_tags = BaseImageTags()
        cell_dict = {
            'title': title,
            'params': self.cell_params,
            'secrets': self.cell_secrets,
            'inputs': self.cell_inputs,
            'outputs': self.cell_outputs,
            'confs': self.cell_confs,
            'dependencies': self.cell_dependencies,
            'base_container_image':
                base_image_tags.base_image_tags[self.base_image_name],
            'chart_obj': chart,
            'kernel': self.kernel
        }
        return Cell.model_validate(cell_dict)

    @abc.abstractmethod
    def get_cell_inputs(self) -> list[dict]:
        pass

    @abc.abstractmethod
    def get_cell_outputs(self) -> list[dict]:
        pass

    @abc.abstractmethod
    def get_cell_params(self) -> list[dict]:
        pass

    @abc.abstractmethod
    def get_cell_secrets(self) -> list[dict]:
        pass

    @abc.abstractmethod
    def get_cell_confs(self) -> list[dict]:
        pass

    @abc.abstractmethod
    def get_cell_dependencies(self, confs) -> list[dict]:
        pass


class DummyExtractor(Extractor):
    def get_cell_inputs(self) -> list[dict]:
        return []

    def get_cell_outputs(self) -> list[dict]:
        return []

    def get_cell_params(self) -> list[dict]:
        return []

    def get_cell_secrets(self) -> list[dict]:
        return []

    def get_cell_confs(self) -> list[dict]:
        return []

    def get_cell_dependencies(self, confs) -> list[dict]:
        return []
