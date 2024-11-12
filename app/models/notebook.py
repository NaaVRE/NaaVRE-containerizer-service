import logging

from pydantic import BaseModel

from app.models.notebook_cell import NotebookCell

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class Notebook(BaseModel):
    cells: list[NotebookCell]
    metadata: dict
    nbformat: int
    nbformat_minor: int

    def __init__(self, **data):
        super().__init__(**data)
