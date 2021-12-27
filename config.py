import os
from dotenv import load_dotenv

load_dotenv()

SQLALCHEMY_TRACK_MODIFICATIONS = False

# Database config
PGUSER = os.environ.get("PGUSER", "user")
PGPASSWORD = os.environ.get("PGPASSWORD", "pass")
PGDATABASE = os.environ.get("PGDATABASE", "hp")
DATABASE_URL = os.environ.get("PGDATABASE", "hp")
SQLALCHEMY_DATABASE_URI = DATABASE_URL or (
    f"postgresql://{PGUSER}:{PGPASSWORD}@localhost:5432/{PGDATABASE}"
)

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
HOST_URL = "http://localhost:8080"
