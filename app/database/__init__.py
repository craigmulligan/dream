from typing import Optional, Union, Any
import sqlite3
from flask import g, current_app
from app.models import User


class Db:
    context_key = "_db_connection"

    def __init__(self, app) -> None:
        db_url = app.config["DB_URL"]
        connection = sqlite3.connect(db_url)
        connection.row_factory = self.make_dicts
        self.conn = connection

    @staticmethod
    def tear_down(_):
        """
        When app context is torn down
        close the db connection.
        """
        db = getattr(g, Db.context_key, None)
        if db is not None:
            db.conn.close()

    @staticmethod
    def make_dicts(cursor, row):
        return dict(
            (cursor.description[idx][0], value) for idx, value in enumerate(row)
        )

    def setup(self):
        """
        initializes schema
        """
        self.conn.execute(
            """
            CREATE TABLE IF NOT EXISTS user (id INTEGER PRIMARY KEY, email TEXT UNIQUE NOT NULL , created_at TEXT DEFAULT "datetime('now')" NOT NULL);
        """
        )

        self.conn.execute(
            """
            CREATE INDEX IF NOT EXISTS user_email_idx ON user(email);
        """
        )

        self.conn.execute(
            """
            CREATE INDEX IF NOT EXISTS user_created_at_idx ON user(created_at);
        """
        )

    def user_create(self, email) -> User:
        User.validate_email(email)
        user = self.query(
            """
            INSERT INTO user (email) VALUES (?) RETURNING *
            """,
            [email],
            one=True,
        )

        self.conn.commit()
        assert user
        return User(**user)

    def user_get_by_email(self, email: str):
        user = self.query(
            "select * from user where email = ? limit 1", [email], one=True
        )
        if user:
            return User(**user)

    def user_get_by_id(self, user_id: int):
        user = self.query(
            "select * from user where id = ? limit 1", [user_id], one=True
        )
        if user:
            return User(**user)

    def query(self, query, query_args=(), one=False) -> Union[Optional[Any], Any]:
        cur = self.conn.execute(query, query_args)
        rv = cur.fetchall()
        cur.close()
        return (rv[0] if rv else None) if one else rv


def register(app):
    app.teardown_appcontext(Db.tear_down)


def get() -> Db:
    db = getattr(g, Db.context_key, None)
    if db is None:
        db = Db(current_app)
        setattr(g, Db.context_key, db)

    return db
