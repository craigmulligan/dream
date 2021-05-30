import app
from pytest import fixture
from chalice.test import Client


@fixture
def test_client():
    with Client(app.app) as client:
        yield client
