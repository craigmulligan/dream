from app import api
from app import database
from app.celery import celery
from app import cli
from app.types import FlaskApp


def create_app(settings=None):
    app = FlaskApp(__name__)
    app.config.from_object("config")

    if settings:
        app.config.update(settings)

    # All modules have .init_app()
    # interface.
    database.register(app)
    celery.register(app)
    api.register(app)
    cli.register(app)

    return app
