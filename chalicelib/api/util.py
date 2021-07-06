from chalice import Blueprint

blueprint = Blueprint(__name__)


@blueprint.route("/ping", methods=["GET"])
def ping():
    return {"message": "pong" }