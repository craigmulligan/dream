from chalice import Chalice
from api import register_blueprints

app = Chalice(app_name="app")
register_blueprints(app)
