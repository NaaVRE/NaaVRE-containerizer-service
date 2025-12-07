import json
import logging
import os
import uuid
from time import sleep

import requests
import yaml
from fastapi.testclient import TestClient

from app.main import app, _get_containerizer
from app.models.containerizer_payload import ContainerizerPayload

if os.path.exists('resources'):
    base_path = 'resources'
elif os.path.exists('app/tests/resources/'):
    base_path = 'app/tests/resources/'
else:
    raise RuntimeError('cannot find test resources')

client = TestClient(app)

logging.basicConfig(level=logging.DEBUG)

auth_token = os.getenv('AUTH_TOKEN')


def download_files_from_github(repo_url, download_path):
    repo_owner = repo_url.split('/')[3]
    repo_name = repo_url.split('/')[4]
    branch = repo_url.split('/')[6]
    directory = repo_url.split('/')[7]
    list_url = (f"https://api.github.com/repos/{repo_owner}/{repo_name}"
                f"/contents/{directory}?ref={branch}")
    response = requests.get(list_url)
    if response.status_code == 200:
        for item in response.json():
            if item["type"] == "file":
                file_url = item["download_url"]
                file_response = requests.get(file_url)
                if file_response.status_code == 200:
                    # Save the file in the download path
                    file_name = item["name"]
                    file_path = os.path.join(download_path, file_name)
                    with open(file_path, 'wb') as f:
                        f.write(file_response.content)
                else:
                    raise Exception("Failed to fetch file. Status Code:",
                                    file_response.status_code, "Response:",
                                    file_response.text)
    else:
        raise Exception("Failed to fetch files. Status Code:",
                        response.status_code, "Response:", response.text)


def wait_for_containerization(workflow_id=None,
                              virtual_lab=None,
                              wait_for_completion=True):
    containerization_status_response = client.get(
        '/status/' +
        virtual_lab + '/' +
        workflow_id,
        headers={'Authorization': 'Bearer ' + os.getenv('AUTH_TOKEN')},
    )
    sleep_time = 4
    count = 0
    while containerization_status_response.status_code != 200 and \
            count <= 50:
        print(f"Retrying status check for workflow_id: {workflow_id}")
        sleep(sleep_time)
        containerization_status_response = client.get(
            '/status/' +
            virtual_lab + '/' +
            workflow_id,
            headers={'Authorization': 'Bearer ' + os.getenv('AUTH_TOKEN')},
        )
        count += 1
        sleep_time += 2
    if wait_for_completion:
        sleep_time = 4
        count = 0
        while (containerization_status_response.json()['job']['status'] !=
               'completed' and count <= 50):
            sleep(sleep_time)
            containerization_status_response = client.get(
                '/status/' +
                virtual_lab + '/' +
                workflow_id,
                headers={'Authorization': 'Bearer ' + os.getenv('AUTH_TOKEN')},
            )
            assert containerization_status_response.status_code == 200
            count += 1
            sleep_time += 1
        assert (containerization_status_response.json()['job']['status'] ==
                'completed')
        assert containerization_status_response.json()['job'][
                   'conclusion'] == 'success'
    return containerization_status_response


def gen_tests_reference():
    notebook_cells_dir = os.path.join(base_path, 'notebook_cells')
    cells_dirs = [f.path for f in os.scandir(notebook_cells_dir) if f.is_dir()]
    for cell_dir in cells_dirs:
        cell_path = os.path.join(cell_dir, 'cell.json')
        with open(cell_path) as f:
            cell = json.load(f)

        payload_path = os.path.join(cell_dir, 'payload_containerize.json')
        with open(payload_path) as f:
            containerize_payload = json.load(f)

        containerize_payload['cell'] = cell
        containerize_payload = ContainerizerPayload(**containerize_payload)

        containerizer = _get_containerizer(containerize_payload)
        cell_source_dir = os.path.join(cell_dir, 'containerized_cell_source')
        os.makedirs(cell_source_dir)

        task_source = containerizer.build_script()
        task_filename = os.path.join(
            cell_source_dir, 'task' + containerizer.file_extension)
        with open(task_filename, 'w') as f:
            f.write(task_source)

        environment_source = containerizer.build_environment()
        environment_filename = os.path.join(
            cell_source_dir, 'environment.yaml')
        with open(environment_filename, 'w') as f:
            f.write(environment_source)

        dockerfile_source = containerizer.build_docker()
        dockerfile_filename = os.path.join(cell_source_dir, 'Dockerfile')
        with open(dockerfile_filename, 'w') as f:
            f.write(dockerfile_source)


class RefContainerizer:
    def __init__(self, cell_dir):
        self.source_dir = os.path.join(cell_dir, 'containerized_cell_source')

    def build_script(self, file_extension):
        filename = os.path.join(self.source_dir, 'task' + file_extension)
        with open(filename) as f:
            source = f.read()
        return source

    def build_docker(self):
        filename = os.path.join(self.source_dir, 'Dockerfile')
        with open(filename) as f:
            source = f.read()
        return source

    def build_environment(self):
        filename = os.path.join(self.source_dir, 'environment.yaml')
        with open(filename) as f:
            source = f.read()
        return source


def test_containerize_render():
    notebook_cells_dir = os.path.join(base_path, 'notebook_cells')
    cells_dirs = [f.path for f in os.scandir(notebook_cells_dir) if f.is_dir()]
    for cell_dir in cells_dirs:
        print("Testing containerization for cell", cell_dir)
        cell_path = os.path.join(cell_dir, 'cell.json')
        with open(cell_path) as f:
            cell = json.load(f)

        payload_path = os.path.join(cell_dir, 'payload_containerize.json')
        with open(payload_path) as f:
            containerize_payload = json.load(f)

        containerize_payload['cell'] = cell
        containerize_payload = ContainerizerPayload(**containerize_payload)

        containerizer = _get_containerizer(containerize_payload)

        # Helper to load saved references for containerized cell source
        ref_containerized = RefContainerizer(cell_dir)

        # Compare uild script (task.py or task.R)
        script = containerizer.build_script()
        ref_script = ref_containerized.build_script(
            containerizer.file_extension
            )
        assert ref_script == script

        # Dockerfile
        dockerfile = containerizer.build_docker()
        ref_dockerfile = ref_containerized.build_docker()
        assert dockerfile == ref_dockerfile

        # Compare environment source (environment.yaml) to reference.
        # Because the order in which dependencies are listed might change, we
        # convert them to sets before comparing.
        environment = yaml.safe_load(containerizer.build_environment())
        ref_environment = yaml.safe_load(ref_containerized.build_environment())
        dependencies = sorted(filter(
            lambda x: not isinstance(x, dict),
            environment['dependencies']))
        ref_dependencies = sorted(filter(
            lambda x: not isinstance(x, dict),
            ref_environment['dependencies']))
        assert dependencies == ref_dependencies
        pip_dependencies = list(filter(
            lambda x: isinstance(x, dict),
            environment['dependencies']))
        ref_pip_dependencies = list(filter(
            lambda x: isinstance(x, dict),
            ref_environment['dependencies']))
        assert pip_dependencies == ref_pip_dependencies
        del environment['dependencies']
        del ref_environment['dependencies']
        assert environment == ref_environment


def test_containerize_github(cell_dir):
    os.environ['DEBUG'] = 'True'
    cell_path = os.path.join(cell_dir, 'cell.json')
    with open(cell_path) as f:
        print('Testing containerize for cell: ' + cell_path)
        cell = json.load(f)

    payload_path = os.path.join(cell_dir, 'payload_containerize.json')
    with open(payload_path) as f:
        print('                with payload: ' + payload_path)
        containerizer_json_payload = json.load(f)

    containerizer_json_payload['cell'] = cell
    containerizer_json_payload['force_containerize'] = True
    containerize_response = client.post(
        '/containerize/',
        headers={'Authorization': 'Bearer ' + auth_token},
        json=containerizer_json_payload,
    )
    try:
        assert containerize_response.status_code == 200
    except AssertionError:
        print(
            f"Assertion failed at line "
            f"{__import__('inspect').currentframe().f_lineno - 3}: "
            f"status_code={containerize_response.status_code}")
        logging.error(
            f"Assertion failed at line "
            f"{__import__('inspect').currentframe().f_lineno - 3}: "
            f"status_code={containerize_response.status_code}")
        raise

    workflow_id = containerize_response.json()['workflow_id']
    assert 'source_url' in containerize_response.json()
    source_url = containerize_response.json()['source_url']
    assert 'title' in cell
    assert cell['title'] in source_url
    containerization_status_response = wait_for_containerization(
        workflow_id=workflow_id,
        virtual_lab=containerizer_json_payload['virtual_lab'],
        wait_for_completion=False)
    try:
        assert containerization_status_response.status_code == 200
    except AssertionError:
        print(f"Failed for workflow_id: {workflow_id}")
        logging.info(f"Failed for workflow_id: {workflow_id}")
        print(
            f"Assertion failed at line "
            f"{__import__('inspect').currentframe().f_lineno - 3}: "
            f"status_code={containerization_status_response.status_code}")
        logging.error(
            f"Assertion failed at line "
            f"{__import__('inspect').currentframe().f_lineno - 3}: "
            f"status_code={containerization_status_response.status_code}")
        raise
    containerization_status_response = wait_for_containerization(
        workflow_id=workflow_id,
        virtual_lab=containerizer_json_payload['virtual_lab'],
        wait_for_completion=True)

    try:
        assert (containerization_status_response.json()['job']['status'] ==
                'completed')
    except AssertionError:
        print(f"Failed for workflow_id: {workflow_id}")
        logging.info(f"Failed for workflow_id: {workflow_id}")
        print(
            f"Assertion failed at line "
            f"{__import__('inspect').currentframe().f_lineno - 3}: "
            f"status_code={containerization_status_response.status_code}")
        logging.error(
            f"Assertion failed at line "
            f"{__import__('inspect').currentframe().f_lineno - 3}: "
            f"status_code={containerization_status_response.status_code}")
        raise

    try:
        assert containerization_status_response.json()['job'][
                   'conclusion'] == 'success'
    except AssertionError:
        print(f"Failed for workflow_id: {workflow_id}")
        logging.info(f"Failed for workflow_id: {workflow_id}")
        print(
            f"Assertion failed at line "
            f"{__import__('inspect').currentframe().f_lineno - 3}: "
            f"status_code={containerization_status_response.status_code}")
        logging.error(
            f"Assertion failed at line "
            f"{__import__('inspect').currentframe().f_lineno - 3}: "
            f"status_code={containerization_status_response.status_code}")
        raise
    # Download files from source_url
    download_path = os.path.join('/tmp', 'downloaded_files')
    os.makedirs(download_path, exist_ok=True)
    download_files_from_github(source_url, download_path)

    # Check if the downloaded files are correct
    if (cell['kernel'].lower() == 'python' or
            cell['kernel'] == 'ipython'):
        assert os.path.exists(os.path.join(download_path, 'task.py'))
    elif cell['kernel'].lower() == 'irkernel' or \
            cell['kernel'].lower() == 'r':
        assert os.path.exists(os.path.join(download_path, 'task.R'))
    # assert task_code in cell['original_source']
    assert os.path.exists(os.path.join(download_path, 'environment.yaml'))
    assert os.path.exists(os.path.join(download_path, 'Dockerfile'))

    containerizer_json_payload.update({'force_containerize': False})
    containerize_response = client.post(
        '/containerize/',
        headers={'Authorization': 'Bearer ' + auth_token},
        json=containerizer_json_payload,
    )
    try:
        assert containerize_response.status_code == 200
    except AssertionError:
        print(f"Failed for workflow_id: {workflow_id}")
        logging.info(f"Failed for workflow_id: {workflow_id}")
        print(
            f"Assertion failed at line "
            f"{__import__('inspect').currentframe().f_lineno - 3}: "
            f"status_code={containerize_response.status_code}")
        logging.error(
            f"Assertion failed at line "
            f"{__import__('inspect').currentframe().f_lineno - 3}: "
            f"status_code={containerize_response.status_code}")
        raise

    try:
        assert containerize_response.json()[
                   'dispatched_github_workflow'] is False
    except AssertionError:
        print(f"Failed for workflow_id: {workflow_id}")
        logging.info(f"Failed for workflow_id: {workflow_id}")
        print(
            f"Assertion failed at line "
            f"{__import__('inspect').currentframe().f_lineno - 3}: "
            f"status_code={containerize_response.status_code}")
        logging.error(
            f"Assertion failed at line "
            f"{__import__('inspect').currentframe().f_lineno - 3}: "
            f"status_code={containerize_response.status_code}")
        raise

    uid = str(uuid.uuid4())
    containerizer_json_payload['cell']['title'] = 'test_containerize'+uid
    containerizer_json_payload['force_containerize'] = True
    containerize_response = client.post(
        '/containerize/',
        headers={'Authorization': 'Bearer ' + auth_token},
        json=containerizer_json_payload,
    )

    try:
        assert containerize_response.status_code == 200
    except AssertionError:
        print(f"Failed for workflow_id: {workflow_id}")
        logging.info(f"Failed for workflow_id: {workflow_id}")
        print(
            f"Assertion failed at line "
            f"{__import__('inspect').currentframe().f_lineno - 3}: "
            f"status_code={containerize_response.status_code}")
        logging.error(
            f"Assertion failed at line "
            f"{__import__('inspect').currentframe().f_lineno - 3}: "
            f"status_code={containerize_response.status_code}")
        raise

    workflow_id = containerize_response.json()['workflow_id']
    source_url = containerize_response.json()['source_url']
    assert cell['title'] in source_url
    containerization_status_response = wait_for_containerization(
        workflow_id=workflow_id,
        virtual_lab=containerizer_json_payload['virtual_lab'],
        wait_for_completion=True)

    try:
        assert containerization_status_response.status_code == 200
    except AssertionError:
        print(f"Failed for workflow_id: {workflow_id}")
        logging.info(f"Failed for workflow_id: {workflow_id}")
        print(
            f"Assertion failed at line "
            f"{__import__('inspect').currentframe().f_lineno - 3}: "
            f"status_code={containerization_status_response.status_code}")
        logging.error(
            f"Assertion failed at line "
            f"{__import__('inspect').currentframe().f_lineno - 3}: "
            f"status_code={containerization_status_response.status_code}")
        raise
    try:
        assert (containerization_status_response.json()['job']['status'] ==
                'completed')
    except AssertionError:
        print(f"Failed for workflow_id: {workflow_id}")
        logging.info(f"Failed for workflow_id: {workflow_id}")
        print(
            f"Assertion failed at line "
            f"{__import__('inspect').currentframe().f_lineno - 3}: "
            f"status_code={containerization_status_response.status_code}")
        logging.error(
            f"Assertion failed at line "
            f"{__import__('inspect').currentframe().f_lineno - 3}: "
            f"status_code={containerization_status_response.status_code}")
        raise
    try:
        assert containerization_status_response.json()['job'][
                   'conclusion'] == 'success'
    except AssertionError:
        print(f"Failed for workflow_id: {workflow_id}")
        logging.info(f"Failed for workflow_id: {workflow_id}")
        print(
            f"Assertion failed at line "
            f"{__import__('inspect').currentframe().f_lineno - 3}: "
            f"status_code={containerization_status_response.status_code}")
        logging.error(
            f"Assertion failed at line "
            f"{__import__('inspect').currentframe().f_lineno - 3}: "
            f"status_code={containerization_status_response.status_code}")
        raise
    # Download files from source_url
    download_path = os.path.join('/tmp', 'downloaded_files')
    os.makedirs(download_path, exist_ok=True)
    download_files_from_github(source_url, download_path)

    # Check if the downloaded files are correct
    if (cell['kernel'].lower() == 'python' or
            cell['kernel'] == 'ipython'):
        assert os.path.exists(os.path.join(download_path, 'task.py'))
    elif cell['kernel'].lower() == 'irkernel' or \
            cell['kernel'].lower() == 'r':
        assert os.path.exists(os.path.join(download_path, 'task.R'))
    # assert task_code in cell['original_source']
    assert os.path.exists(os.path.join(download_path, 'environment.yaml'))
    assert os.path.exists(os.path.join(download_path, 'Dockerfile'))
