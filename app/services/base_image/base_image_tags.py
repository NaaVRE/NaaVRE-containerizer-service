import logging
import os

import requests

logger = logging.getLogger('base_image_tags')


class BaseImageTags:
    def __init__(self):
        self.base_image_tags = self._download_base_image_tags()

    @staticmethod
    def _download_base_image_tags():
        url = os.getenv('BASE_IMAGE_TAGS_URL')
        if not url:
            raise ValueError('BASE_IMAGE_TAGS_URL is not set')
        try:
            res = requests.get(url)
            res.raise_for_status()
            return res.json()
        except (
                requests.ConnectionError,
                requests.HTTPError,
                requests.JSONDecodeError,
        ) as e:
            msg = f'Error loading base image tags from {url}\n{e}'
            logger.debug(msg)

    def get(self):
        return self.base_image_tags
