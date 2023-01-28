import pytest
from unittest.mock import Mock

from sqlalchemy_utils.functions import drop_database, create_database, database_exists
from app import create_app
from app.database import db as _db, alembic
from app.models import User
from app.session import session
from app.mail import MailManager
from celery import Task
from flask import g


@pytest.fixture(autouse=True)
def monkey_patch_celery_async(monkeypatch):
    """
    This ensures that celery tasks are called locally
    so you can assert their results within the test
    without running the worker.
    """
    monkeypatch.setattr("celery.Task.apply_async", Task.apply)

@pytest.fixture(autouse=True)
def app(request):
    """Session-wide test `Flask` application."""
    # Suffix the db name with test for tests.
    test_database_uri = "sqlite://"
    # Use in-memory sqlite db for tests
    app = create_app({"SQLALCHEMY_DATABASE_URI": test_database_uri, "TESTING": True, "ENV": "test"})

    if database_exists(test_database_uri):
        drop_database(test_database_uri)

    create_database(test_database_uri)

    # Establish an application context before running the tests.
    ctx = app.app_context()
    ctx.push()

    def teardown():
        drop_database(test_database_uri)
        ctx.pop()

    request.addfinalizer(teardown)
    return app


@pytest.fixture(autouse=True)
def db():
    """migrate the db"""
    alembic.upgrade()
    return _db


@pytest.fixture(scope="function")
def dummy_user(db):
    """
    util function to create a test case user.
    """
    def create_dummy_user(email="x@x.com") -> User:
        user = User(email=email)
        db.session.add(user)
        db.session.commit()
        return user

    return create_dummy_user


@pytest.fixture()
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


@pytest.fixture(autouse=True)
def mail_manager_mock():
    """
    We never want to send real emails in our test suite.
    This replaces it with a Mock so you can assert it was called.
    """
    mock = Mock()
    setattr(g, MailManager.context_key, mock)
    print(mock)
    return mock 
