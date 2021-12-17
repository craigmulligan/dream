from typing import Type
from flask import Flask
from app.database.flask_celery import FlaskCelery

from app.api import register_blueprints
from app.database import db, celery
from app.cli import register_cli

class FlaskApp(Flask):
    """Custom flask app with extensions"""
    celery: Type[FlaskCelery]

def create_app():
    app = FlaskApp(__name__)
    app.config.from_object("config")

    db.init_app(app)
    celery.init_app(app)
    register_blueprints(app)
    register_cli(app, db)

    return app
