
from pydantic import BaseModel
import json
import logging
import re
from typing import Literal
from typing import Optional
from slugify import slugify

from app.models.cell import Cell


class ContainerizerPayload(BaseModel):
    cell: Cell | None = None


    def __init__(self, **data):
        super().__init__(**data)


