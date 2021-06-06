from chalice import Chalice, Response
from chalice.test import Client

app = Chalice(app_name="dream")


@app.route("/xyz")
def index():
    return {"hello": "world"}


@app.route("/", methods=["GET", "POST"])
def index():
    return {"hello": "world"}


@app.on_sns_message(topic="MyDemoTopic")
def handle_sns_message(event):
    app.log.debug(
        "Received message with subject: %s, message: %s", event.subject, event.message
    )


@app.route(
    "/{api_version}/functions/{function_name}/invocations",
    methods=["GET", "POST"],
    content_types=["application/x-amz-json-1.0"],
)
def proxy(api_version, function_name):
    print("local lambda proxy", api_version, function_name)
    print(app.current_request.raw_body)
    print(app.current_request.headers)
    with Client(app) as client:
        res = client.http.get("/")

    return Response(res.body, status_code=res.status_code, headers=res.headers)
