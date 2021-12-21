from sqlalchemy import Column, Integer
from sqlalchemy_utils import (
    EmailType,
    Timestamp,
)
from app.database import BaseModel
from itsdangerous import URLSafeSerializer
from flask import current_app


class User(BaseModel, Timestamp):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(EmailType)

    def get_sigin_token(self):
        signer = URLSafeSerializer(current_app.config["SECRET_KEY"], salt="signin")
        return signer.dumps(self.id)

    @staticmethod
    def verify_sigin_token(token):
        signer = URLSafeSerializer(current_app.config["SECRET_KEY"], salt="signin")
        return signer.loads(token)
