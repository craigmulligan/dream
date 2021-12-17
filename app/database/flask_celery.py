from celery import Celery, signals, Task


class FlaskCelery(Celery):
    def __init__(self):
        super().__init__()

    def init_app(self, app):
        self.conf.update({
            "broker_url": app.config["CELERY_BROKER_URL"],
            "result_backend": app.config["CELERY_RESULT_BACKEND"]
        })

        class ContextTask(Task):
            def __call__(self, *args, **kwargs):
                with app.app_context():
                    return self.run(*args, **kwargs)

        self.Task = ContextTask

        app.celery = self
        return self


@signals.setup_logging.connect
def setup_celery_logging(**_):
    """
    This is to override celeries logging hijack.
    see: https://github.com/celery/celery/issues/2509#issuecomment-153936466
    """
    pass
