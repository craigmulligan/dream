from typing import Optional
from flask import session as flask_session
from app.models import User


class Session:
    """
    wrapper around flask.session
    """

    flask_session = None

    @property
    def session(self):
        if self.flask_session is None:
            return flask_session
        return self.flask_session

    def signin(self, user: User) -> None:
        self.session["user_id"] = user.id

    def is_authenticated(self) -> bool:
        return "user_id" in self.session

    def get_authenticated_user_id(self) -> Optional[int]:
        return self.session.get("user_id")


session = Session()
