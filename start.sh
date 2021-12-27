#!/bin/bash
set -e


set -e
set -m # to make job control work
flask db upgrade &&
gunicorn "run_app:app" -b 0.0.0.0:8080 &
celery -A "run_app:app.celery" worker
fg %1
