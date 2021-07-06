from chalice import Blueprint, Response
from chalicelib.database import session_scope
from chalicelib.templates import templates

blueprint = Blueprint(__name__)


@blueprint.route("/signin", methods=["GET"])
def signin():
    template = templates.get_template("signin.html")

    # request = blueprint.current_request
    return Response(body=template.render(),
                    status_code=200,
                    headers={'Content-Type': 'text/html'})
