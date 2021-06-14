from chalice import Blueprint
from chalicelib.models import User
from chalicelib.schemas import UserSchema
from chalicelib.database import session_scope

blueprint = Blueprint(__name__)

user_schema = UserSchema()


@blueprint.route("/signin", methods=["POST"])
def signin():

    return { "ya":"oh" }
