from app.api.user import blueprint as user
from app.api.auth import blueprint as auth


def register_blueprints(app):
    app.register_blueprint(auth, url_prefix="/auth")
    app.register_blueprint(user, url_prefix="/user")

    @app.route("/")
    def home():
        return "hello world", 200
