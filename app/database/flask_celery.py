from celery import Celery, signals, Task


class FlaskCelery(Celery):
    def __init__(self):
        super().__init__()

    def init_app(self, app):
        self.conf.update(
            {
                "broker_url": "sqla+" + app.config["SQLALCHEMY_DATABASE_URI"],
                "result_backend": "db+" + app.config["SQLALCHEMY_DATABASE_URI"],
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

        app.celery = self
        return self


@signals.setup_logging.connect
def setup_celery_logging(**_):
    """
    This is to override celeries logging hijack.
    see: https://github.com/celery/celery/issues/2509#issuecomment-153936466
    """
    pass
