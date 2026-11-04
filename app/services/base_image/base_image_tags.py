import logging

import cachetools.func
import requests

logger = logging.getLogger('base_image_tags')


class BaseImageTags:
    def __init__(self, base_image_tags_url,
                 find_latest_existing_tag=False):
        self.base_image_tags = self._download_base_image_tags(
            base_image_tags_url,
            find_latest_existing_tag=find_latest_existing_tag)

    @staticmethod
    @cachetools.func.ttl_cache(ttl=6 * 3600)
    def _download_base_image_tags(base_image_tags_url=None,
                                  find_latest_existing_tag=False):
        try:
            res = requests.get(base_image_tags_url)
            if res.status_code == 404 and find_latest_existing_tag:
            # Get redirected URL if the original URL is redirected
                if res.history:
                    redirected_url = res.url
                    # Find the version number in the redirected URL
                    version_number = redirected_url.split('/')[-2]
                    # Construct the new URL with the previous version number ('v0.3.27' -> v.3.26)
                    previous_version_number = 'v' + str(int(version_number[1:]) - 1)
                    new_url = redirected_url.replace(version_number, previous_version_number)
            res.raise_for_status()
            return res.json()
        except (
                requests.ConnectionError,
                requests.HTTPError,
                requests.JSONDecodeError,
        ) as e:
            logger.debug(f'Error loading base image tags from '
                         f'{base_image_tags_url}\n{e}')
            raise IOError('Error loading base image tags')

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
