# TODO user supervisor instead.
#!/bin/bash
set -e
set -m # to make job control work

gunicorn "run_app:app" -b 0.0.0.0:8080 & celery --app "run_app:celery" worker
fg %1
