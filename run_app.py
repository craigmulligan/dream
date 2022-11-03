from app import create_app
from app import celery
import logging

logging.basicConfig(level=logging.INFO)

app = create_app()
# Ensure db schema is up to date.
__all__ = ("celery", "app")
