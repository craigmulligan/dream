from chalice.test import Client
from app import app

def test_foo_function():
    with Client(app) as client:
        result = client.lambda_.invoke('index')
        assert result.payload == {'hello': 'world'}
