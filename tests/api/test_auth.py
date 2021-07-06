from chalicelib.models import User
from chalicelib.templates import templates
import json

#  def test_signin(test_client, session):
    #  assert session.query(User).count() == 0
    #  password = "1234"
    #  user = User(email="x@x.com", password=password)
    #  session.add(user)
    #  session.commit()

    #  body = json.dumps({"id": user.id, "password": password }
    #  response = test_client.http.post(f"/auth/signin")
    #  assert response.status_code == 200 


def test_get_signin(test_client):
    template = templates.get_template("signin.html")
    response = test_client.http.get(f"/auth/signin")
    assert response.status_code == 200
    assert response.body.decode("utf-8") == template.render()
