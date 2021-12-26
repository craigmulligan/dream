import os

SQLALCHEMY_TRACK_MODIFICATIONS = False
PGUSER = os.environ.get("PGUSER", "user")
PGPASSWORD = os.environ.get("PGPASSWORD", "pass")
PGDATABASE = os.environ.get("PGDATABASE", "hp")

SQLALCHEMY_DATABASE_URI = f"postgresql://{PGUSER}:{PGPASSWORD}@localhost:5432/{PGDATABASE}"
SECRET_KEY = "super-secret-key"
BASE_URL = "http://localhost:8080"
