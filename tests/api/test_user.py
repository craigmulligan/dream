from models import User
import json


def test_get_user(test_client, session):
    user = User(name="hobochild")

    session.add(user)
    session.commit()

    response = test_client.http.get(f"/user/{user.id}")
    payload = json.loads(response.body)
    payload["id"] == user.id
