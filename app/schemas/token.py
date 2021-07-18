from marshmallow import Schema, fields, post_load
from lib.models import Token


class TokenSchema(Schema):
    id = fields.Integer()
    email = fields.String()

    @post_load
    def m(self, data, **kwargs):
        return Token(**data)
