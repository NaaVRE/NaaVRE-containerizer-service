import json
import os

from fastapi.testclient import TestClient

from app.main import app

if os.path.exists('resources'):
    base_path = 'resources'
elif os.path.exists('app/tests/resources/'):
    base_path = 'app/tests/resources/'
client = TestClient(app)


def test_extract_cell():
    cells_json_path = os.path.join(base_path, 'notebooks')
    notebooks_files = os.listdir(cells_json_path)
    for notebook_file in notebooks_files:
        if 's6-geotiff-export-local-user.json' not in notebook_file:
            continue
        notebook_path = os.path.join(cells_json_path, notebook_file)
        with open(notebook_path) as f:
            print('Testing extract for notebook: ' + notebook_file)
            notebook_cell = json.load(f)
        f.close()
        extractor_json_payload = notebook_cell.copy()
        del extractor_json_payload['cell']
        expected_cell = notebook_cell['cell']
        cell_extractor_response = client.post(
            '/extract_cell/',
            headers={'Authorization': 'Bearer ' + os.getenv('AUTH_TOKEN')},
            json=extractor_json_payload,
        )
        assert cell_extractor_response.status_code == 200
        cell = cell_extractor_response.json()
        # We don't need to compare the chart_obj
        del cell['chart_obj']
        del expected_cell['chart_obj']
        print('Expected cell: ' + str(expected_cell))
        print('Extracted cell: ' + str(cell))
        assert cell == expected_cell
