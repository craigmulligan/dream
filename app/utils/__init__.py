from http.cookies import SimpleCookie
from itsdangerous import URLSafeSerializer
from lib.schemas import TokenSchema

signer = URLSafeSerializer("secret key", "auth")
token_schema = TokenSchema()


class Cookie:
    # TODO make return types consistent?
    @staticmethod
    def get(request):
        value = request.headers.get("cookie").get("token").value
        return token_schema.loads(signer.loads(value))

    @staticmethod
    def set(user):
        token = signer.dumps(token_schema.dumps(user))
        return SimpleCookie(f"token={token}")
