from flask import Flask

from app.api import register_blueprints
from app.database import db, migrate, celery


def create_app():
    app = Flask(__name__)
    app.config.from_object("config")

    db.init_app(app)
    celery.init_app(app)
    migrate.init_app(app, db)
    register_blueprints(app)

    return app
