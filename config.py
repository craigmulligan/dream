import os

SQLALCHEMY_TRACK_MODIFICATIONS = False
PGUSER = os.environ.get("PGUSER", "user")
PGPASSWORD = os.environ.get("PGPASSWORD", "pass")
PGDATABASE = os.environ.get("PGDATABASE", "hp")

DATABASE_URL=f"postgresql://{PGUSER}:{PGPASSWORD}@postgres:5432/{PGDATABASE}"
SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']
CELERY_BROKER_URL="sqla+" + os.environ['DATABASE_URL']
CELERY_RESULT_BACKEND="db+" + os.environ['DATABASE_URL']
