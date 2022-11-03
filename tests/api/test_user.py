from flask import render_template
from app.models import User


def test_user_get_authenticated(client, dummy_user, signin):
    """
    Asserts user page is correctly rendered.
    """
    user = dummy_user()
    signin(user)

    response = client.get(f"/user/{user.id}")
    assert response.status_code == 200
    assert render_template("user.html", user=user) == response.data.decode("utf-8")


def test_user_get_forbidden(client, dummy_user, signin):
    """
    Asserts a user can not view another user page.
    """
    john = dummy_user(email="john@x.com")
    jane = dummy_user(email="jane@x.com")
    signin(john)

    response = client.get(f"/user/{jane.id}")
    assert response.status_code == 403


def test_user_get_does_not_exist(client, dummy_user, signin):
    """
    Asserts a 404 is returned for a non-existent user.
    """
    user = dummy_user()
    signin(user)

    response = client.get(f"/user/104")
    assert response.status_code == 404


def test_user_get_unauthenticated(client, dummy_user):
    """
    Asserts if the requestor is not logged in
    they are redirected to the signin page.
    """
    user = dummy_user()
    response = client.get(f"/user/{user.id}")
    assert response.status_code == 302
