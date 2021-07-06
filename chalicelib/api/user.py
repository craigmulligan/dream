from chalice import Blueprint
from chalicelib.models import User
from chalicelib.schemas import UserSchema
from chalicelib.database import session_scope

blueprint = Blueprint(__name__)

user_schema = UserSchema()


@blueprint.route("/{user_id}", methods=["GET"])
def get_user(user_id):
    with session_scope() as session:
        user = session.query(User).filter_by(id=user_id).first()
        return user_schema.dump(user)
