import json
import os
from time import sleep

from fastapi.testclient import TestClient

from app.main import app

if os.path.exists('resources'):
    base_path = 'resources'
elif os.path.exists('app/tests/resources/'):
    base_path = 'app/tests/resources/'
client = TestClient(app)


def test_containerize():
    cells_json_path = os.path.join(base_path, 'cells')
    cells_files = os.listdir(cells_json_path)
    for cell_file in cells_files:
        cell_path = os.path.join(cells_json_path, cell_file)
        with open(cell_path) as f:
            print('Testing containerize for cell: ' + cell_file)
            containerizer_payload = json.load(f)
        f.close()
        containerize_response = client.post(
            '/containerize/',
            headers={'Authorization': 'Bearer ABC'},
            json=containerizer_payload,
        )
        assert containerize_response.status_code == 200

        workflow_id = containerize_response.json()['workflow_id']
        containerization_status_response = client.get(
            '/containerization-status/' + workflow_id,
            headers={'Authorization': 'Bearer ABC'},
        )
        assert containerization_status_response.status_code == 200
        count = 0
        sleep_time = 10
        while (containerization_status_response.json()['status'] != 'completed'
               and count <= 3):
            sleep(sleep_time)
            containerization_status_response = client.get(
                '/containerization-status/' + workflow_id,
                headers={'Authorization': 'Bearer ABC'},
            )
            assert containerization_status_response.status_code == 200
            count += 1
            sleep_time += 5
        assert containerization_status_response.json()['status'] == 'completed'
        assert containerization_status_response.json()[
                   'conclusion'] == 'success'
