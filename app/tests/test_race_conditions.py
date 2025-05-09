import json
import os
import random
from concurrent.futures import ThreadPoolExecutor

from fastapi.testclient import TestClient

from app.main import app

if os.path.exists('resources'):
    base_path = 'resources'
elif os.path.exists('app/tests/resources/'):
    base_path = 'app/tests/resources/'
client = TestClient(app)


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
