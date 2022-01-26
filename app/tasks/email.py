import logging
from app.database import celery
from flask import current_app
from app.types import FlaskApp
from typing import cast


@celery.task
def email_send(to, subject, body):
    return cast(FlaskApp, current_app).mail_manager.send(to, subject, body)
