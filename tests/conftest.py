import pytest
from unittest.mock import Mock

from app import create_app
from app.models import User
from app.mail import MailManager
from app.session import session
from app import database
from flask import g
from celery import Task


@pytest.fixture(scope="function", autouse=True)
def app():
    """Session-wide test `Flask` application."""
    # Establish an application context before running the tests.
    app = create_app({"DB_URL": ":memory:", "TESTING": True})
    ctx = app.app_context()
    ctx.push()

    yield app

    ctx.pop()


@pytest.fixture(autouse=True)
def mail_manager_mock():
    mock = Mock()

    setattr(g, MailManager.context_key, mock)
    return mock


@pytest.fixture(scope="function", autouse=True)
def db():
    _db = database.get()
    _db.setup()
    return _db


@pytest.fixture(scope="function")
def dummy_user(db):
    """
    util function to create a test case user.
    """

    def create_dummy_user(email="x@x.com") -> User:
        user = db.user_create(email=email)
        return user

    return create_dummy_user


@pytest.fixture(scope="function")
def signin(client):
    """
    util function to create a test case user.
    """

    def inner(user: User) -> None:
        with client.session_transaction() as sesh:
            session.flask_session = sesh
            session.signin(user)
            session.flask_session = None

    return inner


@pytest.fixture(scope="function", autouse=True)
def monkey_patch_celery_async(monkeypatch):
    """
    This ensures that celery tasks are called locally
    so you can assert their results within the test
    without running the worker.
    """
    monkeypatch.setattr("celery.Task.apply_async", Task.apply)
