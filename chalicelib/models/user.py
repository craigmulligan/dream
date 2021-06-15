from sqlalchemy import Column, Integer
from sqlalchemy_utils import (
    EmailType,
    PasswordType,
    Timestamp,
    force_auto_coercion,
    generic_repr,
)
from .base import Base


force_auto_coercion()


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

    def __init__(self, email, password):
        self.email = email
        self.password = password
