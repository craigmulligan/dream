import re
from sqlalchemy import Column, Integer
from sqlalchemy.orm import validates
from sqlalchemy_utils import (
    EmailType,
    Timestamp,
)
from app.database import BaseModel
from itsdangerous import URLSafeSerializer
from flask import current_app, session


class User(BaseModel, Timestamp):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(EmailType)
    email_regex = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"

    def get_signin_token(self):
        """Used for magic links"""
        signer = URLSafeSerializer(current_app.config["SECRET_KEY"], salt="signin")
        return signer.dumps(self.id)

    @staticmethod
    def verify_signin_token(token: str):
        """Verify token - used for magic links"""
        signer = URLSafeSerializer(current_app.config["SECRET_KEY"], salt="signin")
        return signer.loads(token)

    def can_view(self):
        return session["user_id"] == self.id

    @validates("email")
    def validate_email(self, _, address):
        if not re.fullmatch(self.email_regex, address):
            raise ValueError("Invalid Email")

        return address
