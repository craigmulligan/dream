import pytest

from sqlalchemy_utils.functions import drop_database, create_database, database_exists
from flask_migrate import Migrate, upgrade

from app import create_app
from app.database import db as _db
from app.models import User

from tests.transaction_manager import TransactionManager


@pytest.fixture(scope="session")
def app(request):
    """Session-wide test `Flask` application."""
    app = create_app()

    test_database_uri = app.config["DATABASE_URL"]

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


@pytest.fixture(scope="session", autouse=True)
def db(app):
    """Session-wide test database."""

    _db.app = app

    # Apply migrations to the database
    Migrate(app, _db)
    upgrade()

    return _db


@pytest.fixture(scope="function", autouse=True)
def transact(db, app):
    trans_manager = TransactionManager(db, app)
    trans_manager._start_transaction()

    yield

    trans_manager._close_transaction()


@pytest.fixture(scope="function")
def dummy_user(db):
    """
    util function to create a test case user.
    """

    def create_dummy_user(email="x@x.com"):
        user = User(email=email)
        db.session.add(user)
        db.session.commit()
        return user

    return create_dummy_user


@pytest.fixture(scope="function")
def signin_user(client):
    """
    util function to create a test case user.
    """

    def login(user: User) -> None:
        with client.session_transaction() as session:
            session["user_id"] = user.id

    return login
