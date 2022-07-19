from application import app
from flask import Flask, render_template, url_for, request, session, flash, redirect
import requests
import json
from seed_creator.mnemonic import Mnemonic
from bip32 import BIP32 # https://github.com/darosior/python-bip32


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
    mn_all = mn.to_mnemonic(repeat_word=repeat_word, mnemonic_size=12)
    tot = len(mn_all)
    mn_single = mn_all[0]
    mn_all = [x.split()[-1] for x in mn_all] # just pull last word
    mn_all = " ".join(mn_all)
    seed = mn.to_bip39seed(mn_single)
    master_prvkey = mn.master_prv(seed)
    master_cc = mn.master_chain(seed)


    bip32 = BIP32.from_seed(seed)
    root_xprv = bip32.get_xpriv_from_path("m")
    root_xpub = bip32.get_xpub_from_path("m")
    pub, pubc = mn.to_public(master_prvkey)

    message = f"<p><b>Mnemonic</b>: {mn_single}</p>"
    message += f"<p><b>BIP39 Seed</b>: {seed.hex()}</p>"
    message += f"<p><b>Master Private Key</b>: {master_prvkey.hex()}</p>"
    message += f"<p><b>Master Public Key</b>: {pub.hex()}</p>"
    message += f"<p><b>Master Public Key compressed</b>: {pubc.hex()}</p>"
    message += f"<p><b>Master Chain Code</b>: {master_cc.hex()}</p>"
    message += f"<p><b>BIP32 Root Key</b>: {root_xprv}</p>"

    # BIP 44: m / purpose' / coin_type' / account' / change / address_index
    bip44_prv = bip32.get_xpriv_from_path("m/44'/0'/0'/0")
    bip44_pub = bip32.get_xpub_from_path("m/44'/0'/0'/0")
    message += f"<p><b>Extended Private Key(m/44'/0'/0'/0)</b>: {bip44_prv}</p>"
    message += f"<p><b>Extended Public Key(m/44'/0'/0'/0)</b>: {bip44_pub}</p>"

    pubkey = bip32.get_pubkey_from_path("m/44'/0'/0'/0/0")
    message += f"<p><b>Public Key(m/44'/0'/0'/0/0)</b>: {pubkey.hex()}</p>"
    addr = mn.to_address(pubkey).decode("ascii")
    message += f"<p><b>Address(m/44'/0'/0'/0/0)</b>: {addr}</p>"
    pubkey = bip32.get_pubkey_from_path("m/44'/0'/0'/0/1")
    addr = mn.to_address(pubkey).decode("ascii")
    message += f"<p><b>Address(m/44'/0'/0'/0/1)</b>: {addr}</p>"

    return render_template("mnemonic.html", mn_single=mn_single, mn_all=mn_all, tot=tot)


