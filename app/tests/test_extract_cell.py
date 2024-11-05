import json
import os

from fastapi.testclient import TestClient

from app.main import app
from app.models.workflow_cell import Cell

if os.path.exists('resources'):
    base_path = 'resources'
elif os.path.exists('app/tests/resources/'):
    base_path = 'app/tests/resources/'
client = TestClient(app)


def test_extract_cell():
    cells_json_path = os.path.join(base_path, 'notebooks')
    notebooks_files = os.listdir(cells_json_path)
    for notebook_file in notebooks_files:
        notebook_path = os.path.join(cells_json_path, notebook_file)
        # if ('read-file-lines-r-dev-user-name-domain-com.json'
        #         not in notebook_file):
        #     continue
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
        assert cell_extractor_response.status_code == 200
        cell_dict = cell_extractor_response.json()
        # We don't need to compare the chart_obj
        del cell_dict['chart_obj']
        del expected_cell_dict['chart_obj']
        returned_cell = Cell.model_validate(cell_dict)
        expected_cell = Cell.model_validate(expected_cell_dict)

        returned_cell_confs = returned_cell.confs
        expected_cell_confs = expected_cell.confs
        for returned_conf in returned_cell_confs:
            assert returned_conf in expected_cell_confs
        assert returned_cell.title == expected_cell.title
        assert returned_cell.kernel == expected_cell.kernel

        returned_cell_inputs = returned_cell.inputs
        expected_cell_inputs = expected_cell.inputs
        for returned_input in returned_cell_inputs:
            assert returned_input in expected_cell_inputs

        returned_cell_outputs = returned_cell.outputs
        expected_cell_outputs = expected_cell.outputs
        for returned_output in returned_cell_outputs:
            assert returned_output in expected_cell_outputs

        returned_cell_params = returned_cell.params
        expected_cell_params = expected_cell.params
        for returned_param in returned_cell_params:
            assert returned_param in expected_cell_params

        returned_cell_secrets = returned_cell.secrets
        expected_cell_secrets = expected_cell.secrets
        for returned_secret in returned_cell_secrets:
            assert returned_secret in expected_cell_secrets

        returned_cell_dependencies = returned_cell.dependencies
        expected_cell_dependencies = expected_cell.dependencies
        for returned_dependency in returned_cell_dependencies:
            assert returned_dependency in expected_cell_dependencies

        assert (returned_cell.base_container_image == expected_cell.
                base_container_image)