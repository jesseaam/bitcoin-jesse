from application import app
from flask import Flask, render_template, url_for
import requests
import json


@app.route("/")
def index():
    height = requests.get("https://blockstream.info/api/blocks/tip/height")
    height = height.text

    current_price = requests.get("https://www.bitstamp.net/api/v2/ticker/btcusd/")
    current_price = json.loads(current_price.text)["last"]

    # how many sats can you buy with a dollar?
    sats = round(100_000_000 / float(current_price))

    return render_template("index.html", height=height, price=current_price, sats=sats)

@app.route("/login/", methods=["POST", "GET"])
def login():
    return render_template("login.html")