from flask import Blueprint, render_template, abort
from app.models import User
from app.tasks.audit import audit_log
from app.api.utils import authenticated_resource

blueprint = Blueprint("user", __name__)


@blueprint.route("/<int:user_id>", methods=["GET"])
@authenticated_resource
def get_user(user_id):
    audit_log.delay("user_view", user_id)
    user = User.query.filter_by(id=user_id).one_or_none()

    if not user:
        abort(404)

    return render_template("user.html", user=user)


@blueprint.route("/", methods=["GET"])
def get_users():
    audit_log.delay("users_view", "xyz")
    users = User.query.limit(10).all()
    return render_template("users.html", users=users)
