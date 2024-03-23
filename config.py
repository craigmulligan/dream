import os
from dotenv import load_dotenv

load_dotenv()

SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_DATABASE_URI = os.environ.get("SQLALCHEMY_DATABASE_URI") or os.environ.get("DATABASE_URL") or "sqlite:///app.db"

# Mail config
MAIL_HOST = os.environ.get("MAIL_HOST")
MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD")
MAIL_PORT = int(os.environ.get("MAIL_PORT", 465))
MAIL_USERNAME = os.environ.get("MAIL_USERNAME")
MAIL_FROM = os.environ.get("MAIL_FROM")

# General
# Key used for signing.
SECRET_KEY = "super-secret-key"
# DNS name of the server.
HOST_URL = os.environ.get("HOST_URL", "http://localhost:8080")
ENV=os.environ.get("ENV")
