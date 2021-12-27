import logging
from app.database import celery
from flask import current_app


@celery.task
def email_send(to, subject, body):
    return current_app.mail_manager.send(to, subject, body)
