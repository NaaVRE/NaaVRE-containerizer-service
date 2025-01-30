import json
import os
from time import sleep
import subprocess
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

        containerizer_payload = {'cell': cell_notebook_dict['cell']}

        containerize_response = client.post(
            '/containerize/',
            headers={'Authorization': 'Bearer ' + os.getenv('AUTH_TOKEN')},
            json=containerizer_payload,
        )
        assert containerize_response.status_code == 200

        workflow_id = containerize_response.json()['workflow_id']
        source_url = containerize_response.json()['source_url']
        containerization_status_response = client.get(
            '/containerization-status/' + workflow_id,
            headers={'Authorization': 'Bearer ' + os.getenv('AUTH_TOKEN')},
        )
        assert containerization_status_response.status_code == 200
        count = 0
        sleep_time = 10
        while (containerization_status_response.json()['status'] != 'completed'
               and count <= 30):
            sleep(sleep_time)
            containerization_status_response = client.get(
                '/containerization-status/' + workflow_id,
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
            test_r_script_syntax(os.path.join(download_path, 'task.R'))

        assert os.path.exists(os.path.join(download_path, 'environment.yaml'))
        assert os.path.exists(os.path.join(download_path, 'Dockerfile'))


def test_r_script_syntax(r_script_path: str = None):
    command = ["R", "-e", f"source('{r_script_path}', echo=TRUE)"]
    # Run the command
    result = subprocess.run(command, capture_output=True, text=True)

    # Check if the command was successful (exit code 0 means no syntax errors)
    assert result.returncode == 0, f"R script syntax error:\n{result.stderr}"
