import re
from itsdangerous import URLSafeTimedSerializer
from flask import current_app, session


class User:
    email_regex = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"
    salt_signin = "signin"
    id: int
    email: str
    created_at: str

    def __init__(self, *, id: int, email: str, created_at: str) -> None:
        if None in (id, email):
            raise Exception("Invalid user")

        self.id = id
        self.email = email
        self.created_at = created_at

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

    @staticmethod
    def validate_email(address):
        if not re.fullmatch(User.email_regex, address):
            raise ValueError("Invalid Email")

        return address
