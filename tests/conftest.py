import app
from pytest import fixture
from chalice.test import Client
from chalicelib.database import session_scope, engine
from sqlalchemy.event import listens_for


@fixture
def test_client():
    with Client(app.app) as client:
        yield client


@fixture(scope="function")
def session():
    # https://stackoverflow.com/questions/53371410/sqlalchemy-session-management-in-test-agnostic-functions
    connection = engine.connect()

    # begin a non-ORM transaction
    transaction = connection.begin()

    # bind an individual Session to the connection
    with session_scope(bind=connection) as session:
        ###    optional     ###
        # if the database supports SAVEPOINT (SQLite needs special
        # config for this to work), starting a savepoint
        # will allow tests to also use rollback within tests
        nested = connection.begin_nested()

        @listens_for(session, "after_transaction_end")
        def resetart_savepoint(sess, trans):
            if trans.nested and not trans._parent.nested:
                session.expire_all()
                session.begin_nested()

        yield session

        session.close()
        transaction.rollback()
        connection.close()
