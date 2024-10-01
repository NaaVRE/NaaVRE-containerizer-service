from pydantic import BaseModel

from app.models.cell import Cell


class ContainerizerPayload(BaseModel):
    cell: Cell | None = None

    def __init__(self, **data):
        super().__init__(**data)
