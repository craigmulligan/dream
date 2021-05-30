from chalice import Blueprint
from database import engine

blueprint = Blueprint(__name__)


@blueprint.route("/ping", methods=["GET"])
def ping():
    return {"message": "pong"}


@blueprint.route("/ready", methods=["GET"])
def ready():
    with engine.connect() as conn:
        for result in conn.execute("select * from pg_catalog.pg_tables"):
            print(result)

        return {"message": "ready"}
