from application import app
from flask import Flask


@app.route("/")
def index():
    return "<h1>Hello World!</h1>"
