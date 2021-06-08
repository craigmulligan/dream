import logging
import json
from time import sleep
from chalice import Chalice, Response
from chalice.test import Client

app = Chalice(app_name="dream")
# Enable DEBUG logs.
app.log.setLevel(logging.DEBUG)


@app.route("/xyz")
def index():
    return {"hello": "world"}


@app.route("/", methods=["GET", "POST"])
def index():
    return {"hello": "world"}


@app.on_sns_message(topic="audit-log")
def handle_sns_message(event):
    sleep(10)
    app.log.debug(
        "Received message with subject: %s, message: %s", event.subject, event.message
    )
    return {"hello": "world"}


@app.route(
    "/{api_version}/functions/{function_name}/invocations",
    methods=["POST"],
    content_types=["application/x-amz-json-1.0"],
)
def proxy(api_version, function_name):
    print("local lambda proxy", api_version, function_name)
    print(app.current_request.raw_body)
    print(app.current_request.headers)

    event = json.loads(app.current_request.raw_body)

    with Client(app) as client:
        res = client.lambda_.invoke("handle_sns_message", event)

        return Response(res.payload, status_code=200)
