from celery import Celery

class FlaskCelery(Celery):
    def __init__(self):
        super().__init__()

    def init_app(self, app):
        self.conf.broker_url = app.config['CELERY_BROKER_URL']
        self.conf.result_backend = app.config['CELERY_RESULT_BACKEND']
        self.conf.update(app.config)
        self.conf.update(app.config)

        class ContextTask(self.Task):
            def __call__(self, *args, **kwargs):
                with app.app_context():
                    return self.run(*args, **kwargs)

        self.Task = ContextTask

        app.celery = self
        return self
