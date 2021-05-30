from chalice import Chalice
from api.util import blueprint as util
from api.user import blueprint as user

app = Chalice(app_name="app")
app.register_blueprint(util, url_prefix="/util")
app.register_blueprint(user, url_prefix="/user")
