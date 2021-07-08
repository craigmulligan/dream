from chalicelib.models import User
import json


def test_get_user(test_client, session):
    assert session.query(User).count() == 0
    user = User(email="x@x.com", password="1234")
    session.add(user)
    session.commit()

    response = test_client.http.get(f"/user/{user.id}")
    payload = json.loads(response.body)

    assert response.status_code == 200
    assert payload == {
        "id": user.id,
        "email": user.email,
        "created_at": user.created_at,
        "updated_at": user.updated_at,
    }
