import logging

import cachetools.func
import requests

logger = logging.getLogger('base_image_tags')


class BaseImageTags:
    def __init__(self, base_image_tags_url):
        self.base_image_tags = self._download_base_image_tags(
            base_image_tags_url)

    @staticmethod
    @cachetools.func.ttl_cache(ttl=6 * 3600)
    def _download_base_image_tags(base_image_tags_url=None):
        try:
            res = requests.get(base_image_tags_url)
            res.raise_for_status()
            return res.json()
        except (
                requests.ConnectionError,
                requests.HTTPError,
                requests.JSONDecodeError,
        ) as e:
            msg = (f'Error loading base image tags from '
                   f'{base_image_tags_url}\n{e}')
            logger.debug(msg)
            raise Exception(msg) from e

    def get_base_image_tags(self):
        return self.base_image_tags

    def get_base_image_tag(self, base_image_name):
        if base_image_name not in self.base_image_tags:
            raise ValueError(
                f"Base image name '{base_image_name}' not found in "
                f"base image tags. "
                "Please check the base image name or the base image tags URL."
            )
        return self.base_image_tags[base_image_name]
