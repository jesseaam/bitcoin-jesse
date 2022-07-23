from timeit import repeat
from application import app
from flask import Flask, jsonify, render_template, url_for, request, session, flash, redirect
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


#@app.route("/<repeat_word>", methods=["POST", "GET"])
@app.route("/repeat", methods=["POST", "GET"])
def create_repeat_mnemonic(repeat_word="abandon", mnemonic_size=12):
    mn = Mnemonic()

    if request.method == "POST":
        repeat_word = str(request.form.get("Select-Repeat"))
        mnemonic_size = int(request.form.get("Select-Size"))


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


    results = {"BIP39 Seed": seed.hex(),
               "BIP32 Root Key:": root_xprv,
               "Master Private Key": master_prvkey.hex(),
               "Master Chain Code": master_cc.hex(),
               "Master Public Key": pub.hex(),
               "Master Public Key Compressed": pubc.hex(),
               "Public Keys": {"m/44'/0'/0'/0/0": pubkey0.hex() ,
                               "m/44'/0'/0'/0/1": pubkey1.hex()},
               "Addresses":   {"m/44'/0'/0'/0/0": addr0,
                               "m/44'/0'/0'/0/1": addr1}
               }

    print(results)
    results = json.dumps(results, indent=2)
    print(type(results))

    return render_template("display_mnemonic_repeat.html", mn_single=mn_single, mn_all=mn_all, tot=tot, results=results)


@app.route("/random", methods=["POST", "GET"])
def random():
    if request.method == "POST":
        a = Mnemonic()
        ms = int(request.form.get("Select-Size"))
        mn = a.generate_random(mnemonic_size=ms)

        return jsonify(mn)
        #return "<p>Here is where the random mnemonic will be.</p>"


    return render_template("random.html")


@app.route("/resources")
def resources():
    return render_template("resources.html")


@app.route("/whitepaper")
def whitepaper():
    return redirect("https://bitcoin.org/bitcoin.pdf")


@app.route("/repeat-seed")
def repeat_seed():
    codewords = Mnemonic().wordlist
    return render_template("repeat_seed.html", codewords=codewords)


@app.route("/verify-transaction")
def verify_transaction():
    return render_template("verify_transaction.html")


@app.route("/verify-signature")
def verify_signature():
    return render_template("verify_signature.html")