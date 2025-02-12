from pydantic import BaseModel

from app.models.workflow_cell import Cell


class ContainerizerPayload(BaseModel):
    virtual_lab: str
    cell: Cell | None = None

    def __init__(self, **data):
        super().__init__(**data)
