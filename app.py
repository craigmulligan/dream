import logging
from chalice import Chalice
from app.api import register_blueprints

app = Chalice(app_name="app")
app.log.setLevel(logging.DEBUG)

register_blueprints(app)
