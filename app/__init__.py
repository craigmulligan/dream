from typing import Type
from flask import Flask

from app.api import register_blueprints
from app.database import db, celery, FlaskCelery
from app.cli import register_cli
from app.mail import mail_manager, MailManager
from app.types import FlaskApp


def create_app(settings=None):
    app = FlaskApp(__name__)
    app.config.from_object("config")

    if settings:
        app.config.update(settings)

    db.init_app(app)
    celery.init_app(app)
    mail_manager.init_app(app)

    register_blueprints(app)
    register_cli(app, db)

    return app
