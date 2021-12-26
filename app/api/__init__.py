from flask import (
    session,
    redirect,
    url_for,
)

from app.api.user import blueprint as user
from app.api.auth import blueprint as auth


def register_blueprints(app):
    app.register_blueprint(auth, url_prefix="/auth")
    app.register_blueprint(user, url_prefix="/user")

    @app.route("/")
    def _():
        if session.get("user_id"):
            redirect(url_for("user.get_user", user_id=session["user_id"]))

        return redirect(url_for("auth.signin_get"))
