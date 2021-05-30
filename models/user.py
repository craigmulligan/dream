from sqlalchemy import Column, DateTime, Integer, String, create_engine
from sqlalchemy.engine import Connection
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


class User(declarative_base()):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(), default=None)
    created_at = Column(DateTime, default=None)
