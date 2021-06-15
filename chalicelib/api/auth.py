from chalice import Blueprint
from chalicelib.database import session_scope

blueprint = Blueprint(__name__)


@blueprint.route("/signin", methods=["POST"])
def signin():
    return {"ya": "oh"}
