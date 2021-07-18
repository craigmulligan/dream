from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from app.database.flask_celery import FlaskCelery

db = SQLAlchemy()
migrate = Migrate()
celery = FlaskCelery()
