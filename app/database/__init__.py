from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from app.database.flask_celery import FlaskCelery
from flask_alembic import Alembic

class Base(DeclarativeBase):
  pass

db = SQLAlchemy(model_class=Base)

celery = FlaskCelery()
alembic = Alembic()
