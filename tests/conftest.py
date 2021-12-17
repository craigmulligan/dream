import os
from sqlalchemy_utils.functions import drop_database, create_database, database_exists
from app import create_app
import pytest
from pytest import fixture
from flask_migrate import Migrate, upgrade

from app.database import db as _db
from tests.transaction_manager import TransactionManager


@pytest.fixture(scope="session")
def app(request):
    """Session-wide test `Flask` application."""
    app = create_app()

    TEST_DATABASE_URI = app.config["DATABASE_URL"] + "_test"

    if database_exists(TEST_DATABASE_URI):
        drop_database(TEST_DATABASE_URI)

    create_database(TEST_DATABASE_URI)

    # Establish an application context before running the tests.
    ctx = app.app_context()
    ctx.push()

    def teardown():
        ctx.pop()

    request.addfinalizer(teardown)
    return app


@pytest.fixture(scope="session", autouse=True)
def db(app, request):
    """Session-wide test database."""

    _db.app = app

    # Apply migrations to the database
    Migrate(app, _db)
    upgrade()

    return _db


@pytest.fixture(scope="function", autouse=True)
def transact(request, db, app):
    trans_manager = TransactionManager(db, app)
    trans_manager._start_transaction()

    yield

    trans_manager._close_transaction()
