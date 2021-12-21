from flask import (
    Blueprint,
    render_template,
    request,
    flash,
    current_app,
    session,
    redirect,
    url_for,
)
from markupsafe import Markup
from app.models import User
from app.database import db

blueprint = Blueprint("auth", __name__)


@blueprint.route("/signin", methods=["GET"])
def signin_get():
    return render_template("signin.html")


@blueprint.route("/magic", methods=["POST"])
def magic_post():
    email = request.form["email"]
    user = User.query.filter_by(email=email).one_or_none()
    token = None

    if not user:
        # create the user.
        user = User(email=email)
        db.session.add(user)
        db.session.commit()

    token = user.get_sigin_token()

    if current_app.config["ENV"] == "development":
        magic_link = Markup(
            f"<a href='magic?token={token}'>here is your magic link</a>"
        )
        flash(magic_link)
    else:
        # if prod we email.
        pass

    return render_template("magic.html")


@blueprint.route("/magic", methods=["GET"])
def magic_get():
    token = request.args.get("token")
    user_id = User.verify_sigin_token(token)
    session["user_id"] = user_id
    flash("You are now signed in.")
    return redirect(url_for("user.get_user", user_id=user_id))
