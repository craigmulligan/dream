from flask import Blueprint, render_template
from app.models import User

blueprint = Blueprint("user", __name__)


@blueprint.route("/<string:user_id>", methods=["GET"])
def get_user(user_id):
    user = User.query.filter_by(id=user_id).first()
    return render_template("home.html", user=user)
