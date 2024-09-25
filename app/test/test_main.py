import json

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)



def test_read_main():

    #Load payload from resources/cells/Cell-title-test-user.json
    with open('resources/cells/Cell-title-test-user.json') as f:
        payload = json.load(f)
    f.close()

    response = client.post(
        '/containerize/',
        headers={'Authorization:': 'Bearer ABC'},
        json=payload,
    )

    assert response.status_code == 200
    assert response.json() == {'msg': 'Hello World'}

