from typing import List

from pydantic import Field
from pydantic_settings import BaseSettings

from app.models.vl_config import VLConfig


class ServiceSettings(BaseSettings):
    r_built_in: List[str] = Field(default_factory=list)
    vl_configurations: List[VLConfig]


class Settings:
    def __init__(self, config: dict | None = None):
        self.config = config or {}
        self.service_settings = ServiceSettings(**self.config)

    def get_vl_config(self, virtual_lab) -> VLConfig:
        for setting in self.service_settings.vl_configurations:
            if setting.name == virtual_lab:
                return setting
        raise ValueError(f"Virtual lab '{virtual_lab}' not found in settings.")

    def get_r_built_in(self) -> List[str]:
        return self.service_settings.r_built_in
