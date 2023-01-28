from app.database import db, celery, alembic
from app import api
from app import cli
from flask import Flask


def create_app(settings=None):
    app = Flask(__name__)
    app.config.from_object("config")

    if settings:
        app.config.update(settings)

    alembic.init_app(app)
    db.init_app(app)
    celery.init_app(app)
    api.init_app(app)
    cli.init_app(app)

    return app
