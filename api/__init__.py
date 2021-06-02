from .user import blueprint as user
from .util import blueprint as util


def register_blueprints(app):
    @app.middleware("all")
    def my_middleware(event, get_response):
        app.log.info("Before calling my main Lambda function.")
        response = get_response(event)
        app.log.info("After calling my main Lambda function.")
        return response

    app.register_blueprint(util, url_prefix="/util")
    app.register_blueprint(user, url_prefix="/user")
