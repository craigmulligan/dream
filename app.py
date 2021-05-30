from chalice import Chalice
from api.util import blueprint as util

app = Chalice(app_name="dream")
app.register_blueprint(util, url_prefix="/util")
