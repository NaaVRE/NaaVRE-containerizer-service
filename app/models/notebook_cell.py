import logging
from typing import Literal

from pydantic import BaseModel

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class NotebookCell(BaseModel):
    cell_type: Literal['code', 'markdown', 'raw']
    execution_count: int | None = None
    metadata: dict | None = None
    outputs: list | None = None
    source: str | list[str]
