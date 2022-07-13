from application import app
from flask import Flask, render_template, url_for, request, session, flash, redirect
import requests
import json

# add an api
# add blueprints

@app.route("/")
def index():
    height = requests.get("https://blockstream.info/api/blocks/tip/height")
    height = height.text

    current_price = requests.get("https://www.bitstamp.net/api/v2/ticker/btcusd/")
    current_price = json.loads(current_price.text)["last"]

    # how many sats can you buy with a dollar?
    sats = round(100_000_000 / float(current_price))

    if "user" in session:
        user = session["user"]
        message = f"You were successfully logged in {user}!"
        flash(message)
        return render_template("index.html", height=height, price=current_price, sats=sats, user=user, message=message)
    return render_template("index.html", height=height, price=current_price, sats=sats)

@app.route("/login/", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        user = request.form.get("nm")
        session["user"] = user
        return redirect(url_for("index"))
    return render_template("login.html")

@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for('index'))