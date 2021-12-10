from flask import Flask

from app.api import register_blueprints
from app.database import db, celery
from app.cli import register_cli


def create_app():
    app = Flask(__name__)
    app.config.from_object("config")

    db.init_app(app)
    celery.init_app(app)
    register_blueprints(app)
    register_cli(app, db)

    return app
