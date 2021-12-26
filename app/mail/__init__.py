import smtplib, ssl

class MailManagerNotConfigured(Exception):
    pass

class MailManager():
    def init_app(self, app):
        self.email_from = app.config.get("MAIL_FROM")
        self.host = app.config.get("MAIL_HOST")
        self.port = int(app.config.get("MAIL_PORT", 465))
        self.password = app.config.get("MAIL_PASSWORD")
        app.mail_manager = self

    def send(self, to, subject, body):
        if None in (self.email_from, self.host, self.port, self.password):
            raise MailManagerNotConfigured("Ensure you have configured all the required MAIL_* environment variables.")

        message = f"Subject: {subject}\n\n{body}"

        context = ssl.create_default_context()
        with smtplib.SMTP_SSL("smtp.gmail.com", self.port, context=context) as server:
            server.login(self.email_from, self.password)
            server.sendmail(
                self.email_from,
                to,
                message,
            )


mail_manager = MailManager()
