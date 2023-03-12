from flask import Flask, request, make_response
import xmltodict
import logging
from collections import defaultdict
from multiply import multiply

app = Flask(__name__)


@app.route("/soap", methods=["POST"])
def post_multiply():
    result = multiply(request.data)
    resp = make_response(result, 200)
    resp.headers["Content-Type"] = "application/xml, charset=utf-8"
    return resp


@app.route("/")
def index():
    return "<p>Hello, World!</p>"
