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


Session = sessionmaker()
Session.configure(bind=engine)


@contextmanager
def session_scope():
    session = Session()
    try:
        yield session
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()
