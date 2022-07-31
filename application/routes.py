from flask import Flask, jsonify, render_template, url_for, request, session, flash, redirect
from flask_sqlalchemy import SQLAlchemy
import requests, json, datetime
from application import app, db
from seed_creator.mnemonic import Mnemonic
from .models import Mnemonic_db
from .wallets import Wallet
from api.api import basic_api


app.register_blueprint(basic_api, url_prefix="/api")


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


@app.route("/repeat/", methods=["POST", "GET"])
def create_repeat_mnemonic(repeat_word="abandon", mnemonic_size=12):
    if request.method == "GET":
        return redirect(url_for("repeat_seed"))

    if request.method == "POST":
        repeat_word = str(request.form.get("Select-Repeat"))
        mnemonic_size = int(request.form.get("Select-Size"))

    # Get the mnemonic phrase and multiple characteristics of it.
    mn_all, phrase, tot, funded, summary, addr0, results = Wallet.repeat_wallet(repeat_word=repeat_word, mnemonic_size=mnemonic_size)

    # Time at which the mnemonic was created. Populate this in db.
    now = datetime.datetime.now()
    now = now.strftime("%Y-%m-%d %H:%M:%S")

    # add results to db
    db_entry = Mnemonic_db(mnemonic=phrase, addr0=addr0, datetime=now, funded=funded, summary=summary)
    db.session.add(db_entry)
    db.session.commit()

    return render_template("display_mnemonic_repeat.html", mn_single=phrase, mn_all=mn_all, tot=tot, results=results)


@app.route("/random", methods=["POST", "GET"])
def random(ms=12):
    if request.form.get("Select-Size"):
        ms = int(request.form.get("Select-Size"))
        phrase, funded, summary, addr0, results = Wallet.random_wallet(mnemonic_size=ms)

        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        db_entry = Mnemonic_db(mnemonic=phrase, addr0=addr0, funded=funded, summary=summary, datetime=now)
        db.session.add(db_entry)
        db.session.commit()
        return render_template("display_mnemonic_random.html", results=results, phrase=phrase)
    else:
        return render_template("random.html")


#@app.route("/brain-wallet/<phrase>", methods=["GET", "POST"])
@app.route("/brain-wallet/", methods=["GET", "POST"])
def brain_wallet():
    phrase = "hello"
    addr, funded, summary = Wallet.brain_wallet(phrase)
    return jsonify(bw_phrase=phrase, address=addr, funded=funded, summary=summary)


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