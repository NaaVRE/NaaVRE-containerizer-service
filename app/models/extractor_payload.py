from pydantic import BaseModel

from app.models.notebook_data import NotebookData


class ExtractorPayload(BaseModel):
    data: NotebookData | None = None

    def __init__(self, **data):
        super().__init__(**data)
