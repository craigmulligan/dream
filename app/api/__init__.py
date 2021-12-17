from .user import blueprint as user


def register_blueprints(app):
    app.register_blueprint(user, url_prefix="/user")

    @app.route("/")
    def health():
        return "hello world", 200
