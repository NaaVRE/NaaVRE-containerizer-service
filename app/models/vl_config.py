import logging

from pydantic import BaseModel

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class VLConfig(BaseModel):
    name: str
    base_image_tags_url: str
    module_mapping_url: str
    cell_github_url: str
    cell_github_token: str
    registry_url: str
