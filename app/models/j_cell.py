import logging
from typing import Literal, Optional

from pydantic import BaseModel

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class JCell(BaseModel):
    cell_type: Literal['code', 'markdown', 'raw']
    execution_count: int | None = None
    id: str
    metadata: dict | None = None
    outputs: Optional[list] | None = None
    source: str | None = None

    def __init__(self, **data):
        super().__init__(**data)
