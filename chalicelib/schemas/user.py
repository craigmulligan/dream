from chalicelib.models import User
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema


class UserSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = User
        load_instance = True
