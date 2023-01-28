from app.database import celery
from app import mail


@celery.task
def email_send(to, subject, body):
    manager = mail.get_manager()
    return manager.send(to, subject, body)
