from flask import Flask

from app.api import register_blueprints
from app.database import db, migrate


def create_app():
    app = Flask(__name__)
    app.config.from_object("config")

    db.init_app(app)
    register_blueprints(app)
    migrate.init_app(app, db)

    return app

