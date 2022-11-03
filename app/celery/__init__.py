from celery import Celery, signals, Task


class FlaskCelery(Celery):
    ContextTask: Task

    def __init__(self):
        super().__init__()

    def register(self, app):
        self.conf.update(
            {
                "broker_url": "sqla+sqlite:///" + app.config["DB_URL"],
                "result_backend": "db+sqlite:///" + app.config["DB_URL"],
            }
        )

        class ContextTask(Task):
            def __call__(self, *args, **kwargs):
                with app.app_context():
                    return self.run(*args, **kwargs)

        if not app.config.get("TESTING"):
            # In the tests we don't want
            # to push a app context
            # this is because the unit
            # tests already have a context pushed
            # which confuses things.
            self.Task = ContextTask

        return self


@signals.setup_logging.connect
def setup_celery_logging(**_):
    """
    This is to override celeries logging hijack.
    see: https://github.com/celery/celery/issues/2509#issuecomment-153936466
    """
    pass


celery = FlaskCelery()
