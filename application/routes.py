from timeit import repeat
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


@app.route("/<repeat_word>", methods=["POST", "GET"])
def create_repeat_mnemonic(repeat_word, mnemonic_size=12):
    mn = Mnemonic()

    #if request.method == "POST":
    #    repeat_word = request.form.get("Select-Repeat")
    #    mnemonic_size = request.form.get("Select-Size")


    mn_all = mn.to_mnemonic(repeat_word=repeat_word, mnemonic_size=mnemonic_size)
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

    # BIP 44: m / purpose' / coin_type' / account' / change / address_index
    bip44_prv = bip32.get_xpriv_from_path("m/44'/0'/0'/0")
    bip44_pub = bip32.get_xpub_from_path("m/44'/0'/0'/0")
    pubkey0 = bip32.get_pubkey_from_path("m/44'/0'/0'/0/0"); addr0 = mn.to_address(pubkey0).decode("ascii")
    pubkey1 = bip32.get_pubkey_from_path("m/44'/0'/0'/0/1"); addr1 = mn.to_address(pubkey1).decode("ascii")

    return render_template("mnemonic_repeat.html", mn_single=mn_single, mn_all=mn_all, tot=tot, bip39seed=seed.hex(), mprv=master_prvkey.hex(), mpub=pub.hex(), mpubc=pubc.hex(), mcc=master_cc.hex(), bip32root=root_xprv, xprv=bip44_prv, xpub=bip44_pub, pubkey0=pubkey0.hex(), pubkey1=pubkey1.hex(), addr0=addr0, addr1=addr1)


@app.route("/resources")
def resources():
    return render_template("resources.html")


@app.route("/whitepaper")
def whitepaper():
    return redirect("https://bitcoin.org/bitcoin.pdf")


@app.route("/test")
def testpage():
    codewords = Mnemonic().wordlist
    return render_template("test_enter_word.html", codewords=codewords)


@app.route("/verify-transaction")
def verify_transaction():
    return render_template("verify_transaction.html")


@app.route("/test2" , methods=["GET", "POST"])
def test2():
    repeat_word = str(request.form.get("Select-Repeat"))
    mn_size = str(request.form.get("Select-Size"))
    message = f"<h2>{repeat_word}:{mn_size}<h2>"
    return message # just to see what select is