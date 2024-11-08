import logging

from pydantic import BaseModel

from app.models.notebook import Notebook

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class NotebookData(BaseModel):
    cell_index: int
    kernel: str
    notebook: Notebook
    save: bool
    user_name: str | None = None
    base_image_name: str | None = None

    def __init__(self, **data):
        super().__init__(**data)
        if not self.base_image_name:
            self.set_base_image_name()

    def set_user_name(self, user_name: str):
        self.user_name = user_name
        return self

    # We could try a smart way of detecting the dependencies and decide the
    # flavor base image
    def set_base_image_name(self):
        if self.kernel.lower() == "python" or self.kernel == "ipython":
            self.base_image_name = "python"
        elif self.kernel.lower() == "r" or self.kernel.lower() == "irkernel":
            self.base_image_name = "r"
        elif self.kernel.lower() == "julia":
            self.base_image_name = "julia"
        elif self.kernel.lower() == "c":
            self.base_image_name = "c"
