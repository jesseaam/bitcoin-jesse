from flask import Flask, jsonify, render_template, url_for, request, session, flash, redirect
from flask_sqlalchemy import SQLAlchemy
from timeit import repeat
from application import app, db
from .models import Mnemonic_db
import requests
import json
from seed_creator.mnemonic import Mnemonic
from bip32 import BIP32 # https://github.com/darosior/python-bip32
import datetime

# add an api
# add blueprints


# potentially separte this
@app.cli.command("db_create")
def create_all():
    db.create_all()
    print("Database created!")


@app.cli.command("db_drop")
def delete_all():
    db.drop_all()
    print("Database destroyed!")


@app.cli.command("db_seed")
def db_seed():
    mn = Mnemonic()
    phrase = mn.generate_random(mnemonic_size=12)
    seed = mn.to_bip39seed(phrase)
    bip32 = BIP32.from_seed(seed)
    pubkey0 = bip32.get_pubkey_from_path("m/44'/0'/0'/0/0"); addr0 = mn.to_address(pubkey0).decode("ascii")
    funded, summary = mn.summarize_addr(addr0)

    now = datetime.datetime.now()
    now = now.strftime("%Y-%m-%d %H:%M:%S")
    # add results to db
    db_entry = Mnemonic_db(mnemonic=phrase, addr0=addr0,funded=funded,summary=summary,datetime=now)

    db.session.add(db_entry)
    db.session.commit()
    print("Database seeded!")


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


#@app.route("/repeat/<repeat_word>", methods=["POST", "GET"])
@app.route("/repeat/", methods=["POST", "GET"])
def create_repeat_mnemonic(repeat_word="abandon", mnemonic_size=12):
    if request.method == "GET":
        return redirect(url_for("repeat_seed"))
    #if repeat_word == None:

    if request.method == "POST":
        repeat_word = str(request.form.get("Select-Repeat"))
        mnemonic_size = int(request.form.get("Select-Size"))

    mn = Mnemonic()
    mn_all = mn.repeat_mnemonic(repeat_word=repeat_word, mnemonic_size=mnemonic_size)
    tot = len(mn_all)
    mn_single = mn_all[0]
    mn_all = [x.split()[-1] for x in mn_all] # just pull last word
    mn_all = mn_all[1:] # all other possible mns (remove the 1 we're showcasing)
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

    results = json.dumps(results, indent=2)

    funded, summary = mn.summarize_addr(addr0)

    now = datetime.datetime.now()
    now = now.strftime("%Y-%m-%d %H:%M:%S")
    # add results to db
    db_entry = Mnemonic_db(mnemonic=mn_single, addr0=addr0, datetime=now, funded=funded, summary=summary)
    db.session.add(db_entry)
    db.session.commit()
    return render_template("display_mnemonic_repeat.html", mn_single=mn_single, mn_all=mn_all, tot=tot, results=results)


@app.route("/random", methods=["POST", "GET"])
def random(ms=12):
    if request.method == "POST":
        mn = Mnemonic()
        if request.form.get("Select-Size"):
            ms = int(request.form.get("Select-Size"))
        
        phrase = mn.generate_random(mnemonic_size=ms)
        seed = mn.to_bip39seed(phrase)

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

        results = {"Mnemonic": phrase,
                   "BIP39 Seed": seed.hex(),
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

        results = json.dumps(results, indent=2)

        funded, summary = mn.summarize_addr(addr0)

        now = datetime.datetime.now()
        now = now.strftime("%Y-%m-%d %H:%M:%S")
        # add results to db
        db_entry = Mnemonic_db(mnemonic=phrase, addr0=addr0,funded=funded,summary=summary,datetime=now)
        db.session.add(db_entry)
        db.session.commit()
        return render_template("display_mnemonic_random.html", results=results, phrase=phrase)
    else:
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


@app.route("/raw-tx")
def raw_tx():
    return render_template("transaction_structure.html")


@app.route("/view-db")
def view_db():
    all_mn = Mnemonic_db.query.all()
    return render_template("view_db.html", db=all_mn)


@app.route("/delete-all")
def delete_all():
    Mnemonic_db.query.delete()
    db.session.commit()
    return redirect(url_for("view_db"))


#@app.route("/check-all")
#def check_all():
#    mn = Mnemonic()
#    wlist = mn.wordlist[:100]
#    for word in wlist:
#        create_repeat_mnemonic(repeat_word=word, mnemonic_size=12)
#    return redirect(url_for("view_db"))