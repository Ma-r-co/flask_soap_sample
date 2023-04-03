from flask import Flask, request, make_response
from .multiply import multiply
from .celsius2fahrenheit import celsius2fahrenheit

app = Flask(__name__)


@app.route("/soap/multiply", methods=["POST"])
def post_multiply():
    result = multiply(request.data)
    resp = make_response(result, 200)
    resp.headers["Content-Type"] = "application/xml, charset=utf-8"
    return resp


@app.route("/soap/c2f", methods=["POST", "GET"])
def post_celsius2fahrenheit():
    message = celsius2fahrenheit(request.data)
    resp = make_response(message, 200)
    resp.headers["Content-Type"] = "application/xml, charset=utf-8"
    return resp


@app.route("/")
def index():
    return "<p>Hello, World!</p>"
