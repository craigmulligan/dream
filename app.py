from chalice import Chalice

app = Chalice(app_name="dream")


@app.route("/xyz")
def index():
    return {"hello": "world"}
