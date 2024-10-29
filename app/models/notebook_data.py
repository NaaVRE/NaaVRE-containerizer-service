import logging

from pydantic import BaseModel

from app.models.notebook import Notebook

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class NotebookData(BaseModel):
    cell_index: int
    kernel: str
    notebook: Notebook
    save: bool

    def __init__(self, **data):
        super().__init__(**data)
