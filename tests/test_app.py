import pytest

from app.app import app


@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


def test_hello_world(client):
    response = client.get('/')
    assert response.data == b'Hello, World!'
    assert response.status_code == 200


def test_mongo_status(client):
    response = client.get('/mongo_status')
    assert response.status_code == 200
