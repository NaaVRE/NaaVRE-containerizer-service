from pydantic import BaseModel

from app.models.workflow_cell import Cell


class ContainerizerPayload(BaseModel):
    virtual_lab: str
    cell: Cell | None = None
    force_containerize: bool = False

    def __init__(self, **data):
        super().__init__(**data)
