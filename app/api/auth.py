from http.cookies import SimpleCookie
from chalice import Blueprint, Response
from requests_toolbelt import MultipartDecoder

from lib.database import session_scope
from lib.templates import templates
from lib.models import User
from lib.database import session_scope
from lib.utils import Cookie

blueprint = Blueprint(__name__)
signin_template = templates.get_template("signin.html")
home_template = templates.get_template("home.html")


@blueprint.route("/signin", methods=["GET"])
def signin_get():
    template = templates.get_template("signin.html")

    if blueprint.current_request.headers.get("Cookie"):
        token = Cookie.get(blueprint.current_request)

        with session_scope() as session:
            user = session.query(User).filter_by(id=token.id).one_or_none()
            # Already signed in.
            if user:
                return Response(
                    body=home_template.render(user=user),
                    status_code=200,
                    headers={"Content-Type": "text/html"},
                )

    return Response(
        body=signin_template.render(),
        status_code=200,
        headers={"Content-Type": "text/html"},
    )


@blueprint.route("/signin", methods=["POST"], content_types=["multipart/form-data"])
def signin_post():
    request = blueprint.current_request
    email, password = MultipartDecoder(
        request.raw_body, request.headers["content-type"]
    ).parts

    with session_scope() as session:
        user = session.query(User).filter_by(email=email.text).one_or_none()

        if user and user.password == password.text:
            # Dump signed user.
            return Response(
                body=home_template.render(user=user),
                status_code=200,
                headers={
                    "Content-Type": "text/html",
                    # TODO improve security
                    "Set-Cookie": [Cookie.set(user).output()],
                },
            )

        return Response(
            body=signin_template.render(error_message="Incorrect email or password."),
            status_code=200,
            headers={"Content-Type": "text/html"},
        )
