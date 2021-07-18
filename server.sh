set -e
flask db upgrade && gunicorn "run_app:app" -b 0.0.0.0:8080
