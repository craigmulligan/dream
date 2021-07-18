from app.models import User
from app.templates import templates
from requests_toolbelt import MultipartEncoder


def test_get_signin(test_client):
    # TODO should redirect
    template = templates.get_template("signin.html")
    response = test_client.http.get(f"/auth/signin")
    assert response.status_code == 200
    assert response.body.decode("utf-8") == template.render()


def test_signin_post(test_client, session):
    template = templates.get_template("home.html")

    assert session.query(User).count() == 0
    password = "1234"
    user = User(email="x@x.com", password=password)
    session.add(user)
    session.commit()

    data = {
        "email": user.email,
        "password": password,
    }

    form = MultipartEncoder(fields=data)
    response = test_client.http.post(
        f"/auth/signin",
        body=form.to_string(),
        headers={"content-type": form.content_type},
    )

    assert response.status_code == 200
    assert response.body.decode("utf-8") == template.render(user=user)
