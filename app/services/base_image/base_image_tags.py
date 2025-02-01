import logging

import requests

logger = logging.getLogger('base_image_tags')


class BaseImageTags:
    def __init__(self, base_image_tags_url):
        self.base_image_tags = self._download_base_image_tags(
            base_image_tags_url)

    @staticmethod
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

    def get(self):
        return self.base_image_tags
