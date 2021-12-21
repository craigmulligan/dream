from flask import render_template, session


def test_get_user_authenticated(client, dummy_user, signin_user):
    user = dummy_user()
    signin_user(user)

    response = client.get(f"/user/{user.id}")
    assert response.status_code == 200
    assert render_template("user.html", user=user) == response.data.decode("utf-8")


def test_get_user_unauthenticated(client, dummy_user):
    """
    Asserts if the requestor is not logged in
    they are redirected to the signin page.
    """
    user = dummy_user()
    response = client.get(f"/user/{user.id}")
    assert response.status_code == 302
