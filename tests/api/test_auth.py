from flask import render_template
from freezegun import freeze_time
from datetime import datetime, timedelta
from app.session import session
from app.models import User
from unittest.mock import patch


def test_post_magic_success_create_user(client, db):
    """
    Asserts user can request signin email by submitting email to /auth/magic
    """
    email = "x@x.com"
    assert not db.user_get_by_email(email)
    response = client.post(
        f"/auth/magic", content_type="multipart/form-data", data=dict(email=email)
    )
    assert response.status_code == 200
    new_user = db.user_get_by_email(email)
    assert new_user.email == email


def test_get_sigin_page(client):
    """
    Asserts signin page is correctly rendered.
    """
    response = client.get(f"/auth/signin")
    assert render_template("signin.html") == response.data.decode("utf-8")


def test_post_magic_success_in_dev_mode(
    client, dummy_user, signin, app, mail_manager_mock
):
    """
    Asserts user can request signin email by submitting email to /auth/magic
    And that in dev mode we render the link to the flash message & DONT
    send a email.
    """
    user = dummy_user()
    signin(user)
    token = user.get_signin_token()

    with patch.dict(app.config, {"DEBUG": "development"}):
        response = client.post(
            f"/auth/magic",
            content_type="multipart/form-data",
            data=dict(email="x@x.com"),
        )
        mail_manager_mock.send.assert_not_called()

        # in dev mode we send the token to the client.
        # check we don't accidently do that here.
        assert token in response.data.decode("utf-8")
        assert render_template("magic.html") == response.data.decode("utf-8")


def test_post_magic_success_prod_mode(
    client, dummy_user, signin, app, mail_manager_mock
):
    """
    Asserts user can request signin email by submitting email to /auth/magic
    """
    user = dummy_user("x@test.com")
    signin(user)
    token = user.get_signin_token()

    response = client.post(
        f"/auth/magic", content_type="multipart/form-data", data=dict(email=user.email)
    )
    host_url = app.config["HOST_URL"]

    mail_manager_mock.send.assert_called_once_with(
        user.email,
        "Signin link",
        f"<a href='{host_url}/auth/magic?token={token}'>Click here to signin.</a>",
    )

    # in dev mode we send the token to the client.
    # check we don't accidently do that here.
    assert token not in response.data.decode("utf-8")
    assert render_template("magic.html") == response.data.decode("utf-8")


def test_post_magic_bad_email(client, app, mail_manager_mock):
    """
    Asserts user can't signin by submitting an invalid email
    """
    response = client.post(
        f"/auth/magic",
        content_type="multipart/form-data",
        data=dict(email="not_an_email"),
    )

    assert response.status_code == 400
    assert "Invalid Email" in response.data.decode("utf-8")
    mail_manager_mock.send.assert_not_called()


def test_post_magic_no_email(client, app, mail_manager_mock):
    """
    Asserts user can't signin by submitting no email
    """
    response = client.post(
        f"/auth/magic",
        content_type="multipart/form-data",
        data=dict(email=""),
    )

    assert response.status_code == 400
    assert "An email address is required to request signin" in response.data.decode(
        "utf-8"
    )
    mail_manager_mock.send.assert_not_called()


def test_get_magic_success(client, dummy_user):
    """
    Asserts user can signin by passing signin token as a query string.
    """
    user = dummy_user()
    token = user.get_signin_token()
    # Check no user is signed in.
    assert not session.is_authenticated()

    response = client.get(
        f"/auth/magic", query_string=dict(token=token), follow_redirects=True
    )
    # in dev mode we send the token to the client.
    # check we don't accidently do that here.
    assert response.status_code == 200
    assert "You are now signed in." in response.data.decode("utf-8")
    # check the session holds the user_id
    assert session.get_authenticated_user_id() == user.id


def test_get_magic_timeout(client, dummy_user):
    """
    Asserts user can signin by passing signin token as a query string.
    """
    user = dummy_user()
    token = user.get_signin_token()
    now = datetime.now()
    hour_later = now + timedelta(hours=1)
    # Check no user is signed in.
    assert not session.is_authenticated()

    # TODO assert email.send called with token link.
    with freeze_time(hour_later):
        response = client.get(
            f"/auth/magic", query_string=dict(token=token), follow_redirects=True
        )
        # Check that we don't allow this.
        assert response.status_code == 403
        assert "Your link has expired" in response.data.decode("utf-8")
        assert not session.is_authenticated()


def test_get_magic_fail(client, dummy_user):
    """
    Asserts user can't use a bad token to signin.
    """
    user = dummy_user()
    bad_token = user.get_signin_token() + "xyz"
    assert not session.is_authenticated()
    response = client.get(f"/auth/magic", query_string=dict(token=bad_token))

    # in dev mode we send the token to the client.
    # check we don't accidently do that here.
    assert response.status_code == 403
    assert not session.is_authenticated()


def test_get_magic_no_token(client, dummy_user):
    """
    Asserts user can't use a bad token to signin.
    """
    user = dummy_user()
    assert not session.is_authenticated()
    response = client.get(f"/auth/magic", query_string=dict(token=None))

    assert response.status_code == 400
    assert not session.is_authenticated()


def test_get_logout(client, dummy_user, signin):
    """
    Asserts the logout link works correctly
    """
    user = dummy_user()
    signin(user)

    response = client.get("/", follow_redirects=True)
    assert render_template("user.html", user=user) == response.data.decode("utf-8")
    assert session.is_authenticated()

    response = client.get(f"/auth/logout", follow_redirects=True)
    assert render_template("signin.html") == response.data.decode("utf-8")
    assert not session.is_authenticated()
