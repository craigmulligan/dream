from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from contextlib import contextmanager
import boto3

client = boto3.client("rds-data", endpoint_url="http://rds")

engine = create_engine(
    "postgresql+pydataapi://",
    echo=True,
    connect_args={
        "resource_arn": "arn:aws:rds:us-east-1:123456789012:cluster:dummy",
        "secret_arn": "arn:aws:secretsmanager:us-east-1:123456789012:secret:dummy",
        "database": "test",
        "client": client,
    },
)


class BindManager:
    """
    Allows us to use a single connection
    for tests or Engine for other sessions.
    """

    def __init__(self):
        self.bind = None

    def get_bind(self, bind=None):
        if bind is not None:
            self.bind = bind

        if self.bind is None:
            self.bind = engine

        return self.bind


bind_manager = BindManager()


@contextmanager
def session_scope(bind=None):
    Session = sessionmaker()
    Session.configure(bind=bind_manager.get_bind(bind=bind))
    session = Session()
    try:
        yield session
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()
