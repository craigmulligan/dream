from sqlalchemy import Column, Integer
from sqlalchemy_utils import (
    EmailType,
    PasswordType,
    Timestamp,
    generic_repr,
)
from app.database import db


@generic_repr
class User(db.Model, Timestamp):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(EmailType)
    password = Column(
        PasswordType(
            schemes=[
                "bcrypt",
            ]
        ),
        nullable=False,
    )
