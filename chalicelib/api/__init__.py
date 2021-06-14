from .user import blueprint as user
from .util import blueprint as util
from .auth import blueprint as auth


def register_blueprints(app):
    app.register_blueprint(util, url_prefix="/util")
    app.register_blueprint(user, url_prefix="/user")
