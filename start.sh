#!/bin/bash
set -e
set -m # to make job control work

flask db upgrade && gunicorn "run_app:app" -b 0.0.0.0:8080 & celery --app "run_app:celery" worker
fg %1
