from typing import List

from pydantic_settings import BaseSettings

from app.models.vl_config import VLConfig


DEFAULT_BUILT_IN_FUNCTION_URL = (
    'https://raw.githubusercontent.com/NaaVRE/NaaVRE-conf/refs/heads/main/'
    'build_in_r_function_names.json'
)


class ServiceSettings(BaseSettings):
    built_in_function_url: str = DEFAULT_BUILT_IN_FUNCTION_URL
    vl_configurations: List[VLConfig]


class Settings:
    def __init__(self, config: dict = None):
        self.config = config
        self.service_settings = ServiceSettings(**config)

    def get_vl_config(self, virtual_lab) -> VLConfig:
        for setting in self.service_settings.vl_configurations:
            if setting.name == virtual_lab:
                return setting
        raise ValueError(f"Virtual lab '{virtual_lab}' not found in settings.")

    def get_built_in_function_url(self):
        return (self.service_settings.built_in_function_url or
                DEFAULT_BUILT_IN_FUNCTION_URL)
