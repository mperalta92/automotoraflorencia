from flask import Blueprint, send_file
import os

NAME = 'images'
page = Blueprint(NAME, __name__)


def initialize_app(app):
    app.register_blueprint(page, url_prefix="/" + NAME)


@page.route("/")
def index():
    return send_file("static/index.html")


@page.route("/<image>")
def images(image):
    try:
        respond = send_file(os.path.join(os.environ['FILES_PATH'], image))
    except FileNotFoundError:
        respond = send_file(os.path.join(os.path.abspath("."), "app/static/index.html"))
    return respond


@page.route("/original/<image>")
def original(image):
    try:
        respond = send_file(os.path.join(os.path.join(os.environ['FILES_PATH'] + '/', IMAGE_FOLDER), image))
    except FileNotFoundError:
        respond = send_file(os.path.join(os.path.abspath("."), "forge_api/static/index.html"))
    return respond


@page.after_app_request
def after_request(response):
    if 'Access-Control-Allow-Origin' not in response.headers:
        response.headers.add('Access-Control-Allow-Origin', '*')
    return response
