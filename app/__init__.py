from flask import Flask

from app.api import register_blueprints
from app.database import db


def create_app(file_name):
    app = Flask(__name__)
    app.config.from_object(file_name)

    db.init_app(app)
    register_blueprints(app)
    return app

