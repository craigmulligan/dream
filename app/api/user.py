from flask import Blueprint, render_template, abort
from app.models import User
from app.api.utils import authenticated_resource
from sqlalchemy import select
from app.database import db

blueprint = Blueprint("user", __name__)


@blueprint.route("/<int:user_id>", methods=["GET"])
@authenticated_resource
def user_get(user_id):
    stmt = select(User).filter_by(id=user_id)
    user = db.session.scalars(stmt).one_or_none()

    if not user:
        abort(404)

    if not user.can_view():
        abort(403)

    return render_template("user.html", user=user)
