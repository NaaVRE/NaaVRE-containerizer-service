import logging
from pydantic import BaseModel
from typing import Literal

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class NotebookCell(BaseModel):
    cell_type: Literal['code', 'markdown', 'raw']
    execution_count: int | None = None
    id: str
    metadata: dict | None = None
    outputs: list | None = None
    source: str
