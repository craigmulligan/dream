from flask import (
    Blueprint,
    render_template,
    request,
    flash,
    session,
    redirect,
    url_for,
    abort,
)
from markupsafe import Markup
from app.models import User
from app.database import db
from app.mail import mail_manager
from app.utils import is_dev
from itsdangerous import BadSignature


blueprint = Blueprint("auth", __name__)


@blueprint.route("/signin", methods=["GET"])
def signin_get():
    return render_template("signin.html")


@blueprint.route("/magic", methods=["POST"])
def magic_post():
    email = request.form["email"]

    if not email:
        abort(400)

    user = User.query.filter_by(email=email).one_or_none()
    token = None

    if not user:
        # create the user.
        try:
            user = User(email=email)
        except ValueError as e:
            abort(400, str(e))

        db.session.add(user)
        db.session.commit()

    token = user.get_signin_token()

    if is_dev():
        magic_link = Markup(
            f"<a href='magic?token={token}'>here is your magic link</a>"
        )
        flash(magic_link)
    else:
        pass
        # TODO send async email

    return render_template("magic.html")


@blueprint.route("/magic", methods=["GET"])
def magic_get():
    token = request.args.get("token")
    if not token:
        abort(400)

    try:
        user_id = User.verify_signin_token(token)
        session["user_id"] = user_id
    except BadSignature:
        abort(403)

    flash("You are now signed in.")
    return redirect(url_for("user.get_user", user_id=user_id))
