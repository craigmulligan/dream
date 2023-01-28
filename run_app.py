from app import create_app
from app import celery
import logging


logging.basicConfig(level=logging.INFO)

app = create_app()
__all__ = ("celery", "app")
