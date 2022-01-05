import re
from sqlalchemy import Column, Integer
from sqlalchemy.orm import validates
from sqlalchemy_utils import (
    EmailType,
    Timestamp,
)
from app.database import BaseModel
from itsdangerous import URLSafeTimedSerializer
from flask import current_app, session


class User(BaseModel, Timestamp):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(EmailType)
    email_regex = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"
    salt_signin = "signin"

    @staticmethod
    def _get_serializer(salt: str) -> URLSafeTimedSerializer:
        """Gets a URLSafeSerializer"""
        return URLSafeTimedSerializer(current_app.config["SECRET_KEY"], salt=salt)

    @staticmethod
    def verify_signin_token(token: str):
        """
        Verify token - used for magic links
        with 30 min expiry.
        """
        return User._get_serializer(User.salt_signin).loads(token, max_age=30 * 60)

    def get_signin_token(self):
        """Used for magic links"""
        return self._get_serializer(User.salt_signin).dumps(self.id)

    def can_view(self):
        return session["user_id"] == self.id

    @validates("email")
    def validate_email(self, _, address):
        if not re.fullmatch(self.email_regex, address):
            raise ValueError("Invalid Email")

        return address
