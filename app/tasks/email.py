from app.celery import celery
from app import mail


@celery.task
def email_send(to, subject, body):
    mail_manager = mail.get()
    return mail_manager.send(to, subject, body)
