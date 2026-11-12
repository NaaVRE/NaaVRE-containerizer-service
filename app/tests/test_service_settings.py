import json
from pathlib import Path

from app.settings.service_settings import (
    DEFAULT_BUILT_IN_FUNCTION_URL,
    Settings,
)


CONFIGURATION_PATH = Path(__file__).resolve().parents[2] / 'configuration.json'


def load_configuration():
    with CONFIGURATION_PATH.open(encoding='utf-8') as configuration_file:
        return json.load(configuration_file)


def test_get_built_in_function_url_uses_configuration_json_value():
    config = load_configuration()
    settings = Settings(config=config)

    assert settings.get_built_in_function_url() == config[
        'built_in_function_url']


def test_get_built_in_function_url_uses_default_when_missing_from_config():
    config = load_configuration()
    config.pop('built_in_function_url', None)
    settings = Settings(config=config)

    assert (settings.get_built_in_function_url() ==
            DEFAULT_BUILT_IN_FUNCTION_URL)
