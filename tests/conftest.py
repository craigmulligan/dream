import app
from pytest import fixture
from chalice.test import Client
from database import session_scope


@fixture
def test_client():
    with Client(app.app) as client:
        yield client


@fixture(scope="function")
def session():
    with session_scope() as session:
        yield session
