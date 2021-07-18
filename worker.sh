set -e
flask db upgrade && celery -A "run_app:app.celery" worker
