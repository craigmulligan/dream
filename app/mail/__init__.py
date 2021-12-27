import smtplib, ssl
from email.message import Message
import logging


class MailManagerNotConfigured(Exception):
    pass


class MailManager:
    def init_app(self, app):
        self.host = app.config.get("MAIL_HOST")
        self.port = app.config.get("MAIL_PORT")
        self.password = app.config.get("MAIL_PASSWORD")
        self.username = app.config.get("MAIL_USERNAME")
        self._from = app.config.get("MAIL_FROM")
        app.mail_manager = self

    def send(self, to, subject, body):
        if None in (self._from, self.host, self.port, self.password, self.username):
            raise MailManagerNotConfigured(
                "Ensure you have configured all the required MAIL_* environment variables."
            )

        logging.info(f"Sending email via {self.host} - {self.username}")

        message = Message()
        message.add_header("from", self._from)
        message.add_header("to", to)
        message.add_header("subject", subject)
        # Always send html emails.
        message.add_header("Content-Type", "text/html")
        message.set_payload(body)

        context = ssl.create_default_context()
        with smtplib.SMTP_SSL(self.host, self.port, context=context) as server:
            server.login(self.username, self.password)
            server.sendmail(self._from, to, message.as_string())


mail_manager = MailManager()
