from typing import TYPE_CHECKING
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from app.database.flask_celery import FlaskCelery

db = SQLAlchemy()

if TYPE_CHECKING:
    # This is needed for the flasksqlamypy plugin.
    from flask_sqlalchemy.model import Model

    BaseModel = db.make_declarative_base(Model)
else:
    BaseModel = db.Model

migrate = Migrate()
celery = FlaskCelery()
