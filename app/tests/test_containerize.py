import json
import logging
import os
import uuid
from time import sleep

import requests
from fastapi.testclient import TestClient

from app.main import app

if os.path.exists('resources'):
    base_path = 'resources'
elif os.path.exists('app/tests/resources/'):
    base_path = 'app/tests/resources/'
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


def test_containerize():
    os.environ['DEBUG'] = 'True'
    cells_json_path = os.path.join(base_path, 'notebook_cells')
    cells_files = os.listdir(cells_json_path)
    for cell_file in cells_files:
        cell_path = os.path.join(cells_json_path, cell_file)
        with open(cell_path) as f:
            print('Testing containerize for cell: ' + cell_file)
            logging.info('Testing containerize for cell: ' + cell_file)
            cell_notebook_dict = json.load(f)
        f.close()

        containerizer_json_payload = cell_notebook_dict.copy()
        del containerizer_json_payload['data']
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
        source_url = containerize_response.json()['source_url']
        assert cell_notebook_dict['cell']['title'] in source_url
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
        if (cell_notebook_dict['cell']['kernel'].lower() == 'python' or
                cell_notebook_dict['cell']['kernel'] == 'ipython'):
            assert os.path.exists(os.path.join(download_path, 'task.py'))
        elif cell_notebook_dict['cell']['kernel'].lower() == 'irkernel' or \
                cell_notebook_dict['cell']['kernel'].lower() == 'r':
            assert os.path.exists(os.path.join(download_path, 'task.R'))
        # assert task_code in cell_notebook_dict['cell'][
        #     'original_source']
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
        assert cell_notebook_dict['cell']['title'] in source_url
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
        if (cell_notebook_dict['cell']['kernel'].lower() == 'python' or
                cell_notebook_dict['cell']['kernel'] == 'ipython'):
            assert os.path.exists(os.path.join(download_path, 'task.py'))
        elif cell_notebook_dict['cell']['kernel'].lower() == 'irkernel' or \
                cell_notebook_dict['cell']['kernel'].lower() == 'r':
            assert os.path.exists(os.path.join(download_path, 'task.R'))
        # assert task_code in cell_notebook_dict['cell'][
        #     'original_source']
        assert os.path.exists(os.path.join(download_path, 'environment.yaml'))
        assert os.path.exists(os.path.join(download_path, 'Dockerfile'))
