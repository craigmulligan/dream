from models import User
import json


def test_get_user(test_client, session):
    session.execute("drop table if exists users;")
    session.execute(
        "create table users (id int not null primary key, name text, created_at TIMESTAMP(6) null);"
    )

    user = User(id=1, name="hobochild")

    session.add(user)
    session.commit()

    response = test_client.http.get(f"/user/{user.id}")
    payload = json.loads(response.body)
    payload["id"] == user.id
