import json
import os
from urllib.parse import quote

import requests
from fastapi.testclient import TestClient

from app.main import app
from app.models.workflow_cell import Cell


if os.path.exists('resources'):
    base_path = 'resources'
elif os.path.exists('app/tests/resources/'):
    base_path = 'app/tests/resources/'
client = TestClient(app)


def test_extract_cell():
    cells_json_path = os.path.join(base_path, 'notebook_cells')
    notebooks_files = os.listdir(cells_json_path)
    for notebook_file in notebooks_files:
        notebook_path = os.path.join(cells_json_path, notebook_file)
        with open(notebook_path) as f:
            print('Testing extract for notebook: ' + notebook_file)
            notebook_cell = json.load(f)
        f.close()

        extractor_json_payload = notebook_cell.copy()
        del extractor_json_payload['cell']
        expected_cell_dict = notebook_cell['cell']
        cell_extractor_response = client.post(
            '/extract_cell/',
            headers={'Authorization': 'Bearer ' + os.getenv('AUTH_TOKEN')},
            json=extractor_json_payload,
        )
        if cell_extractor_response.status_code != 200:
            print(cell_extractor_response.text)
        assert cell_extractor_response.status_code == 200
        cell_dict = cell_extractor_response.json()

        returned_cell = Cell.model_validate(cell_dict)
        expected_cell = Cell.model_validate(expected_cell_dict)

        returned_cell_confs = sorted(returned_cell.confs,
                                     key=lambda x: x['name'])
        expected_cell_confs = sorted(expected_cell.confs,
                                     key=lambda x: x['name'])
        assert (len(returned_cell_confs) == len(expected_cell_confs)), \
            f"Expected {expected_cell_confs}, " \
            f"but got {returned_cell_confs}"

        assert returned_cell.title == expected_cell.title
        assert returned_cell.kernel == expected_cell.kernel

        returned_cell_inputs = sorted(returned_cell.inputs,
                                      key=lambda x: x['name'])
        expected_cell_inputs = sorted(expected_cell.inputs,
                                      key=lambda x: x['name'])

        assert (len(returned_cell_inputs) == len(expected_cell_inputs)), \
            f"Expected {expected_cell_inputs}, " \
            f"but got {returned_cell_inputs}"

        returned_cell_outputs = sorted(returned_cell.outputs,
                                       key=lambda x: x['name'])
        expected_cell_outputs = sorted(expected_cell.outputs,
                                       key=lambda x: x['name'])

        assert (len(returned_cell_outputs) == len(expected_cell_outputs)), \
            f"Expected {expected_cell_outputs}, " \
            f"but got {returned_cell_outputs}"

        returned_cell_params = sorted(returned_cell.params,
                                      key=lambda x: x['name'])
        expected_cell_params = sorted(expected_cell.params,
                                      key=lambda x: x['name'])

        assert (len(returned_cell_params) == len(expected_cell_params)), \
            f"Expected {expected_cell_outputs}, " \
            f"but got {returned_cell_params}"

        returned_cell_secrets = sorted(returned_cell.secrets,
                                       key=lambda x: x['name'])
        expected_cell_secrets = sorted(expected_cell.secrets,
                                       key=lambda x: x['name'])
        assert (len(returned_cell_secrets) == len(expected_cell_secrets)), \
            f"Expected {expected_cell_secrets}, " \
            f"but got {returned_cell_secrets}"

        returned_cell_deps = sorted(returned_cell.dependencies,
                                    key=lambda x: x['name'])
        expected_cell_dependencies = sorted(expected_cell.dependencies,
                                            key=lambda x: x['name'])
        assert (len(returned_cell_deps) == len(expected_cell_dependencies)), \
            f"Expected {expected_cell_dependencies}, " \
            f"but got {returned_cell_deps}"

        assert os.getenv('REGISTRY_TOKEN_FOR_TESTS') is not None, \
            "REGISTRY_TOKEN_FOR_TESTS is not set. "
        tags = get_latest_container_tags_from_ghcr_url(
            expected_cell.base_container_image['build'],
            os.getenv('REGISTRY_TOKEN_FOR_TESTS'))

        # Check if the tags are not None. If None print the name of the image
        assert tags is not None, \
            (f"Failed to fetch tags for "
             f"{expected_cell.base_container_image['build']}")

        expected_cell.base_container_image['build'] = \
            (expected_cell.base_container_image['build'].rsplit(":", 1)[0] +
             f":{tags[0]}")
        expected_cell.base_container_image['runtime'] = \
            (expected_cell.base_container_image['runtime'].rsplit(":", 1)[0] +
             f":{tags[0]}")

        assert (returned_cell.base_container_image == expected_cell.
                base_container_image)
        # In R we add libraries and remove comments
        # assert returned_cell.original_source == expected_cell.original_source


def get_latest_container_tags_from_ghcr_url(ghcr_url, token):
    """
    Given a GHCR image URL, fetch the tags of the latest version of the
    container package.

    Args:
        ghcr_url (str): e.g.
            'ghcr.io/qcdis/naavre/naavre-cell-build-python:latest'
        token (str): GitHub token with 'read:packages' permission

    Returns:
        list: Tags for the latest version or None on error
    """
    try:
        # Parse components
        without_prefix = ghcr_url.replace("ghcr.io/", "")
        parts = without_prefix.split("/")
        org = parts[0]
        package_name_with_tag = "/".join(parts[1:])
        if ":" in package_name_with_tag:
            package_name, _ = package_name_with_tag.rsplit(":", 1)
        else:
            package_name = package_name_with_tag

        # Prepare API request
        encoded_package = quote(package_name, safe='')
        url = (f"https://api.github.com/orgs/{org}/packages/container/"
               f"{encoded_package}/versions")

        headers = {
            "Authorization": f"Bearer {token}",
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28"
        }

        # Send request
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            data = response.json()
            if data:
                return data[0]["metadata"]["container"].get("tags", [])
            else:
                print("No versions found.")
                return None
        else:
            print(f"GitHub API error {response.status_code}: {response.text}")
            return None

    except Exception as e:
        print(f"Error: {e}")
        return None
