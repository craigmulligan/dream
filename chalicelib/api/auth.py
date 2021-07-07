from chalice import Blueprint, Response
from requests_toolbelt import MultipartDecoder

from chalicelib.database import session_scope
from chalicelib.templates import templates
from chalicelib.schemas import UserSchema
from chalicelib.database import session_scope

blueprint = Blueprint(__name__)


@blueprint.route("/signin", methods=["GET"])
def signin_get():
    template = templates.get_template("signin.html")

    return Response(body=template.render(),
                    status_code=200,
                    headers={'Content-Type': 'text/html'})


@blueprint.route("/signin", methods=["POST"], content_types=['multipart/form-data'])
def signin_post():
    template = templates.get_template("home.html")

    request = blueprint.current_request
    email, password = MultipartDecoder(request.raw_body, request.headers['content-type']).parts

    # TODO validate
    user_schema = UserSchema()
    user = user_schema.load({ "email": email.text, "password": password.text })
     
    return Response(body=template.render(user=user),
                    status_code=200,
                    headers={'Content-Type': 'text/html'})
