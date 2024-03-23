from flask import (
    Blueprint,
    render_template,
    request,
    flash,
    session,
    redirect,
    url_for,
    abort,
    current_app,
)
from markupsafe import Markup
from app.models import User
from sqlalchemy import select
from app.database import db
from app.utils import is_dev
from app.tasks import email_send
from itsdangerous import BadSignature, SignatureExpired


blueprint = Blueprint("auth", __name__)


@blueprint.route("/signin", methods=["GET"])
def signin_get():
    return render_template("signin.html")


@blueprint.route("/magic", methods=["POST"])
def magic_post():
    email = request.form["email"]

    if not email:
        abort(400, "An email address is required to request signin")

    stmt = select(User).filter_by(email=email)
    user = db.session.scalars(stmt).one_or_none()
    token = None

    if not user:
        # create the user.
        try:
            user = User(email=email)
        except ValueError as e:
            abort(400, str(e))

        db.session.add(user)
        db.session.commit()

    host_url = current_app.config["HOST_URL"]
    token = user.get_signin_token()
    magic_link = Markup(
        f"<a href='{host_url}/auth/magic?token={token}'>Click here to signin.</a>"
    )

    if is_dev():
        flash(magic_link)
    else:
        email_send.delay(user.email, "Signin link", str(magic_link))

    return render_template("magic.html")


@blueprint.route("/magic", methods=["GET"])
def magic_get():
    token = request.args.get("token")
    if not token:
        abort(400, "A token is required to signin")

    try:
        user_id = User.verify_signin_token(token)
        session["user_id"] = user_id
    except SignatureExpired:
        abort(403, "Your link has expired")

    except BadSignature:
        abort(403)

    flash("You are now signed in.")
    return redirect(url_for("user.user_get", user_id=user_id))


@blueprint.route("/logout", methods=["GET"])
def logout_get():
    del session["user_id"]
    flash("You are now logged out.")
    return redirect(url_for("_"))
