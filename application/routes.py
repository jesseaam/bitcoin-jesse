from application import app
from flask import Flask, render_template, url_for, request, session, flash, redirect
import requests
import json
from seed_creator.mnemonic import Mnemonic

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

@app.route("/<repeat_word>")
def create_repeat_mnemonic(repeat_word):
    mn = Mnemonic()
    mn_single = mn.to_mnemonic(repeat_word=repeat_word, mnemonic_size=12)[0]
    seed = mn.to_bip39seed(mn_single)
    master_prvkey = mn.master_prv(seed)
    master_cc = mn.master_chain(seed)
    root_xprv = mn.to_xprv(master_prvkey, master_cc).decode("utf-8")
    pub, pubc = mn.to_public(master_prvkey)

    message = f"<p><b>Mnemonic</b>: {mn_single}</p>"
    message += f"<p><b>BIP39 Seed</b>: {seed.hex()}</p>"
    message += f"<p><b>Master Private Key</b>: {master_prvkey.hex()}</p>"
    message += f"<p><b>Master Public Key</b>: {pub.hex()}</p>"
    message += f"<p><b>Master Public Key compressed</b>: {pubc.hex()}</p>"
    message += f"<p><b>Master Chain Code</b>: {master_cc.hex()}</p>"
    message += f"<p><b>BIP32 Root Key</b>: {root_xprv}</p>"

    return message


