from flask import render_template, session
from freezegun import freeze_time
from datetime import datetime, timedelta


def test_get_sigin_page(client):
    """
    Asserts signin page is correctly rendered.
    """
    response = client.get(f"/auth/signin")
    assert render_template("signin.html") == response.data.decode("utf-8")


def test_post_magic_success(client, dummy_user, signin_user, app):
    """
    Asserts user can request signin email by submitting email to /auth/magic
    """
    user = dummy_user()
    signin_user(user)
    token = user.get_signin_token()

    response = client.post(
        f"/auth/magic", content_type="multipart/form-data", data=dict(email="x@x.com")
    )
    host_url = app.config["HOST_URL"]

    app.mail_manager.send.assert_called_once_with(
        user.email,
        "Signin link",
        f"<a href='{host_url}/auth/magic?token={token}'>Click here to signin.</a>",
    )

    # in dev mode we send the token to the client.
    # check we don't accidently do that here.
    assert token not in response.data.decode("utf-8")
    assert render_template("magic.html") == response.data.decode("utf-8")


def test_post_magic_bad_email(client, dummy_user, signin_user, app):
    """
    Asserts user can't signin by submitting an invalid email
    """
    user = dummy_user()

    response = client.post(
        f"/auth/magic",
        content_type="multipart/form-data",
        data=dict(email="not_an_email"),
    )

    assert response.status_code == 400
    assert "Invalid Email" in response.data.decode("utf-8")
    app.mail_manager.send.assert_not_called()


def test_get_magic_success(client, dummy_user):
    """
    Asserts user can signin by passing signin token as a query string.
    """
    user = dummy_user()
    token = user.get_signin_token()
    # Check no user is signed in.
    assert not session.get("user_id")

    # TODO assert email.send called with token link.
    response = client.get(
        f"/auth/magic", query_string=dict(token=token), follow_redirects=True
    )

    # in dev mode we send the token to the client.
    # check we don't accidently do that here.
    assert response.status_code == 200
    assert "You are now signed in." in response.data.decode("utf-8")
    # check the session holds the user_id
    assert session["user_id"] == user.id


def test_get_magic_timeout(client, dummy_user):
    """
    Asserts user can signin by passing signin token as a query string.
    """
    user = dummy_user()
    token = user.get_signin_token()
    now = datetime.now()
    hour_later = now + timedelta(hours=1)
    # Check no user is signed in.
    assert not session.get("user_id")

    # TODO assert email.send called with token link.
    with freeze_time(hour_later):
        response = client.get(
            f"/auth/magic", query_string=dict(token=token), follow_redirects=True
        )
        # Check that we don't allow this.
        assert response.status_code == 403
        assert "Your link has expired" in response.data.decode("utf-8")
        assert not session.get("user_id")


def test_get_magic_fail(client, dummy_user):
    """
    Asserts user can't use a bad token to signin.
    """
    user = dummy_user()
    bad_token = user.get_signin_token() + "xyz"
    assert not session.get("user_id")
    response = client.get(f"/auth/magic", query_string=dict(token=bad_token))

    # in dev mode we send the token to the client.
    # check we don't accidently do that here.
    assert response.status_code == 403
    assert not session.get("user_id")


def test_get_logout(client, dummy_user, signin_user):
    """
    Asserts the logout link works correctly
    """
    user = dummy_user()
    signin_user(user)

    response = client.get("/", follow_redirects=True)
    assert render_template("user.html", user=user) == response.data.decode("utf-8")
    assert session.get("user_id")

    response = client.get(f"/auth/logout", follow_redirects=True)
    assert render_template("signin.html") == response.data.decode("utf-8")
    assert not session.get("user_id")
