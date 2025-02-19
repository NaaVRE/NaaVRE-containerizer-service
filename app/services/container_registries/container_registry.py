import json
import os

import requests


class ContainerRegistry:

    def __init__(self, registry_url: str, token: str):
        self.registry_url = registry_url
        if not self.registry_url or 'ghcr.io/' not in registry_url:
            parts = registry_url.split('https://github.com/')
            parts = parts[1].split('/')
            self.registry_url = 'ghcr.io/' + parts[0].lower() + '/' + parts[
                1].replace('.git', '').lower()
        elif 'ghcr.io/' not in registry_url:
            self.owner = self.registry_url.split('/')[0]
        self.token = token

    def query_registry_for_image(self, image_name):
        if 'docker' in self.registry_url:
            # Docker Hub
            url = (f'https://hub.docker.com/v2/repositories/{self.owner}/'
                   f'{image_name}')
            headers = {}
        else:
            # OCI registries
            domain = self.registry_url.split('/')[0]
            path = '/'.join(self.registry_url.split('/')[1:])
            url = f'https://{domain}/v2/{path}/{image_name}/tags/list'
            # OCI registries require authentication, even for public registries
            # The token should be set in the $OCI_TOKEN environment variable.
            # For ghcr.io, connections still succeed when $OCI_TOKEN is unset
            # (this results in header "Authorization: Bearer None", which
            # grants access to public registries, although it is not officially
            # documented). If this fails, or when accessing private registries,
            # OCI_TOKEN should be a base64-encoded GitHub classic access token
            # with the read:packages scope.
            headers = {
                "Authorization": f"Bearer {os.getenv('OCI_TOKEN')}",
            }
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return json.loads(response.content.decode('utf-8'))
        else:
            return None
