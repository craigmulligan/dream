from sqlalchemy import Column, Integer
from sqlalchemy_utils import (
    EmailType,
    PasswordType,
    Timestamp,
    generic_repr,
)
from .base import Base


@generic_repr
class User(Base, Timestamp):
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
