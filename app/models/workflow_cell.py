import logging
from typing import Literal, Optional
from collections.abc import Sequence

from pydantic import BaseModel

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class BaseImage(BaseModel):
    build: str
    runtime: str


class Dependency(BaseModel):
    name: str
    module: Optional[str]
    asname: Optional[str]


class BaseVariable(BaseModel):
    name: str
    type: str | None


class Input(BaseVariable):
    pass


class Output(BaseVariable):
    pass


class Conf(BaseModel):
    name: str
    assignation: str


class Param(BaseVariable):
    default_value: Optional[str]


class Secret(BaseVariable):
    pass


class Cell(BaseModel):
    title: str
    base_container_image: Optional[BaseImage]
    inputs: Sequence[Input]
    outputs: Sequence[Output]
    params: Sequence[Param]
    secrets: Sequence[Secret]
    confs: Sequence[Conf]
    dependencies: Sequence[Dependency]
    kernel: Literal['python', 'IRkernel', 'ipython', 'c']
    original_source: str
    source_url: Optional[str] | None = None
    container_image: Optional[str] | None = None
    description: Optional[str] | None = None

    def __init__(self, **data):
        super().__init__(**data)
