from flask import Blueprint, render_template, abort
from app.models import User
from app.api.utils import authenticated_resource

blueprint = Blueprint("user", __name__)


@blueprint.route("/<int:user_id>", methods=["GET"])
@authenticated_resource
def user_get(user_id):
    user = User.query.filter_by(id=user_id).one_or_none()

    if not user:
        abort(404)

    if not user.can_view():
        abort(403)

    return render_template("user.html", user=user)
