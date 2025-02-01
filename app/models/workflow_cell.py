import logging
from typing import Literal, Optional

from pydantic import BaseModel

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class Cell(BaseModel):
    title: str
    base_container_image: dict
    inputs: Optional[list[dict]] | None = None
    outputs: Optional[list[dict]] | None = None
    params: Optional[list[dict]] | None = None
    secrets: Optional[list[dict]] | None = None
    confs: Optional[list[dict]] | None = None
    dependencies: Optional[list[dict]] | None = None
    chart_obj: dict | None = None
    kernel: Literal['python', 'IRkernel', 'ipython', 'c']
    original_source: str
    source_url: Optional[str] | None = None
    container_image: Optional[str] | None = None
    description: Optional[str] | None = None

    def __init__(self, **data):
        super().__init__(**data)
