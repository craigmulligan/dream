from app import create_app
import logging


logging.basicConfig(level=logging.INFO)

app = create_app()
# Not sure why but celery can't pick up "run_app:app.celery" but can do "run_app:celery"
celery = app.celery
