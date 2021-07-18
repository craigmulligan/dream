from app.models import User
from app.database import db
from flask import render_template


def test_get_user(client, app):
    for rule in app.url_map.iter_rules():
        print(rule)
    assert User.query.count() == 0
    user = User(email="x@x.com", password="1234")
    db.session.add(user)
    db.session.commit()

    response = client.get(f"/user/{user.id}")
    assert response.status_code == 200
    assert render_template("home.html", user=user) == response.data.decode("utf-8")
