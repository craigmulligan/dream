from sqlalchemy import create_engine
import boto3

client = boto3.client("rds-data", endpoint_url="http://rds")

cluster_arn = "arn:aws:rds:us-east-1:123456789012:cluster:dummy"
secret_arn = "arn:aws:secretsmanager:us-east-1:123456789012:secret:dummy"


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
