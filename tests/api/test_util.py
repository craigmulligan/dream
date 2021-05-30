import json


def test_ping(test_client):
    """
    Asserts that we can ping the api.
    """
    response = test_client.http.get("/util/ping")
    data = json.loads(response.body)
    assert data["message"] == "pong"


def test_db_ready(test_client):
    """
    Asserts the db is setup correctly
    """
    response = test_client.http.get("/util/ready")
    data = json.loads(response.body)
    assert data["message"] == "ready"


def test_not_found(test_client):
    """
    Asserts that we get a 403 for an unknown path
    See: https://github.com/aws/chalice/issues/975
    """
    response = test_client.http.get("/util/unknown")
    assert response.status_code == 403
