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
    user_name: str | None = None

    def __init__(self, **data):
        super().__init__(**data)

    def set_user_name(self, user_name: str):
        self.user_name = user_name
        return self
