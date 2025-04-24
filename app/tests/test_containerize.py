import json
import os
import random
from time import sleep
from concurrent.futures import ThreadPoolExecutor
import requests
from fastapi.testclient import TestClient

from app.main import app

if os.path.exists('resources'):
    base_path = 'resources'
elif os.path.exists('app/tests/resources/'):
    base_path = 'app/tests/resources/'
client = TestClient(app)


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


def test_containerize():
    cells_json_path = os.path.join(base_path, 'notebook_cells')
    cells_files = os.listdir(cells_json_path)
    for cell_file in cells_files:
        cell_path = os.path.join(cells_json_path, cell_file)
        with open(cell_path) as f:
            print('Testing containerize for cell: ' + cell_file)
            cell_notebook_dict = json.load(f)
        f.close()

        containerizer_json_payload = cell_notebook_dict.copy()
        del containerizer_json_payload['data']

        containerize_response = client.post(
            '/containerize/',
            headers={'Authorization': 'Bearer ' + os.getenv('AUTH_TOKEN')},
            json=containerizer_json_payload,
        )
        assert containerize_response.status_code == 200

        workflow_id = containerize_response.json()['workflow_id']
        source_url = containerize_response.json()['source_url']
        assert cell_notebook_dict['cell']['title'] in source_url
        containerization_status_response = client.get(
            '/status/' +
            containerizer_json_payload['virtual_lab'] + '/' +
            workflow_id,
            headers={'Authorization': 'Bearer ' + os.getenv('AUTH_TOKEN')},
        )
        assert containerization_status_response.status_code == 200
        count = 0
        sleep_time = 10
        while (containerization_status_response.json()['status'] != 'completed'
               and count <= 30):
            sleep(sleep_time)
            containerization_status_response = client.get(
                '/status/' +
                containerizer_json_payload['virtual_lab'] + '/' +
                workflow_id,
                headers={'Authorization': 'Bearer ' + os.getenv('AUTH_TOKEN')},
            )
            assert containerization_status_response.status_code == 200
            count += 1
            sleep_time += 5
        assert containerization_status_response.json()['status'] == 'completed'
        assert containerization_status_response.json()[
                   'conclusion'] == 'success'
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


def test_race_conditions():
    cells_json_path = os.path.join(base_path, 'notebook_cells')
    cells_files = os.listdir(cells_json_path)
    # Pick a random cell file. Genara a random number between 0 and
    # len(cells_files)
    random_index_1 = random.randint(0, len(cells_files) - 1)
    cell_file_1 = cells_files[random_index_1]
    cell_path_1 = os.path.join(cells_json_path, cell_file_1)
    with open(cell_path_1) as f:
        print('Testing containerize for cell: ' + cell_file_1)
        cell_notebook_dict_1 = json.load(f)
    f.close()
    containerizer_json_payload_1 = cell_notebook_dict_1.copy()
    del containerizer_json_payload_1['data']

    random_index_2 = random.randint(0, len(cells_files) - 1)
    cell_file_2 = cells_files[random_index_2]
    cell_path_2 = os.path.join(cells_json_path, cell_file_2)
    with open(cell_path_2) as f:
        print('Testing containerize for cell: ' + cell_file_2)
        cell_notebook_dict_2 = json.load(f)
    f.close()
    containerizer_json_payload_2 = cell_notebook_dict_2.copy()
    del containerizer_json_payload_2['data']

    # Create a thread to do a POST request to /containerize/ concurrently
    with ThreadPoolExecutor(max_workers=2) as executor:
        futures = [
            executor.submit(make_containerize_request,
                            containerizer_json_payload_1),
            executor.submit(make_containerize_request,
                            containerizer_json_payload_2)
        ]
        results = [f.result() for f in futures]
    for result in results:
        assert result is not None
    print(results)

    # Test it on the same cell
    random_index_3 = random.randint(0, len(cells_files) - 1)
    cell_file_3 = cells_files[random_index_3]
    cell_path_3 = os.path.join(cells_json_path, cell_file_3)
    with open(cell_path_3) as f:
        print('Testing containerize for cell: ' + cell_path_3)
        cell_notebook_dict_3 = json.load(f)
    f.close()
    containerizer_json_payload_3 = cell_notebook_dict_3.copy()
    del containerizer_json_payload_3['data']

    # Create a thread to do a POST request to /containerize/ concurrently
    with ThreadPoolExecutor(max_workers=2) as executor:
        futures = [
            executor.submit(make_containerize_request,
                            containerizer_json_payload_3),
            executor.submit(make_containerize_request,
                            containerizer_json_payload_3)
        ]
        results = [f.result() for f in futures]

    print(results)
    for result in results:
        assert result is not None


def make_containerize_request(payload):
    containerize_response = client.post(
        '/containerize/',
        headers={'Authorization': 'Bearer ' + os.getenv('AUTH_TOKEN')},
        json=payload,
    )
    return containerize_response.json()
