from typing import Type
from flask import Flask
from app.celery import FlaskCelery
from app.mail import MailManager


class FlaskApp(Flask):
    """Custom flask app with extensions"""

    celery: Type[FlaskCelery]
    mail_manager: MailManager
