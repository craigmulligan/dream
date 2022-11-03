#!/bin/bash

# Right now we are just running the server and worker in the same vm 
# This isn't ideal.
# But fly.io + litefs barfs with 2 vms Right now and I'm tired of debugging it.
set -m # to make job control work
gunicorn 'run_app:app' -b 0.0.0.0:8080 &
celery --app 'run_app:celery' worker &
fg %1 # gross!
