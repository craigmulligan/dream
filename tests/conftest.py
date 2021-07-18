import app
from pytest import fixture
from chalice.test import Client
from app.database import session_scope, engine
from sqlalchemy.event import listens_for


@fixture
def test_client():
    with Client(app.app) as client:
        yield client


@fixture(scope="function")
def session():
    connection = engine.connect()

    transaction = connection.begin()

    with session_scope(bind=connection) as session:
        connection.begin_nested()

        @listens_for(session, "after_transaction_end")
        def resetart_savepoint(sess, trans):
            if trans.nested and not trans._parent.nested:
                session.expire_all()
                session.begin_nested()

        yield session

        session.close()
        transaction.rollback()
        connection.close()
