from flask import Blueprint, render_template
from app.models import User
from app.tasks.audit import audit_log

blueprint = Blueprint("user", __name__)


@blueprint.route("/<string:user_id>", methods=["GET"])
def get_user(user_id):
    audit_log.delay("user_view", user_id)
    user = User.query.filter_by(id=user_id).first()
    return render_template("home.html", user=user)


@blueprint.route("/", methods=["GET"])
def get_users():
    audit_log.delay("users_view", "xyz")
    users = User.query.limit(10).all()
    return render_template("users.html", users=users)
