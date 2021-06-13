import logging
from chalice import Chalice
from chalicelib.api import register_blueprints

app = Chalice(app_name="app")
app.log.setLevel(logging.DEBUG)

register_blueprints(app)
