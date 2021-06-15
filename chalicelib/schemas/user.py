from chalicelib.models import User
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema


class UserSchema(SQLAlchemyAutoSchema):
    class Meta:
        load_instance = True
        model = User
