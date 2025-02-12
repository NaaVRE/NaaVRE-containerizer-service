import os

from fastapi.testclient import TestClient

from app.main import app

if os.path.exists('resources'):
    base_path = 'resources'
elif os.path.exists('app/tests/resources/'):
    base_path = 'app/tests/resources/'
client = TestClient(app)


def test_get_base_image_tags():
    labs = ['virtual_lab_1']
    for lab in labs:
        base_image_tags_response = client.get(
            '/base-image-tags?virtual_lab=' + lab,
            headers={'Authorization': 'Bearer ' + os.getenv('AUTH_TOKEN')},
        )
        tags = base_image_tags_response.json()
        assert tags is not None
        assert isinstance(tags, dict)
        for tag in tags:
            assert 'build' in tags[tag]
            assert 'runtime' in tags[tag]
