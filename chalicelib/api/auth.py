from chalice import Blueprint, Response
from requests_toolbelt import MultipartDecoder

from chalicelib.database import session_scope
from chalicelib.templates import templates
from chalicelib.schemas import UserSchema

blueprint = Blueprint(__name__)
user_schema = UserSchema()


@blueprint.route("/signin", methods=["GET"])
def signin_get():
    template = templates.get_template("signin.html")

    return Response(body=template.render(template),
                    status_code=200,
                    headers={'Content-Type': 'text/html'})


@blueprint.route("/signin", methods=["POST"], content_types=['multipart/form-data'])
def signin_post():
    template = templates.get_template("home.html")

    request = blueprint.current_request
    decoder = MultipartDecoder(request.raw_body, request.headers['content-type'])

    # TODO validate
    user = user_schema.load(decoder.parts)
     
    return Response(body=template.render(template, email=user.email),
                    status_code=200,
                    headers={'Content-Type': 'text/html'})
