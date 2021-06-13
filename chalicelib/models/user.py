from sqlalchemy import Column, DateTime, Integer, String
from .base import Base


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(), default=None)
    created_at = Column(DateTime, default=None)
