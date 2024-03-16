from app import data


def test_return_check():
    assert data.healthcheck() == b'Hello, World!'


def test_mongo_status():
    result = data.get_mongo_status()
    assert result['ok'] == 1
