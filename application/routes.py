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
    """Home page that displays btc height & price."""
    height = requests.get("https://blockstream.info/api/blocks/tip/height")
    height = height.text

    #current_price = requests.get("https://www.bitstamp.net/api/v2/ticker/btcusd/")
    #current_price = json.loads(current_price.text)["last"]
    current_price = requests.get("https://api.blockchain.com/v3/exchange/tickers/BTC-USD")
    current_price = json.loads(current_price.text)["last_trade_price"]

    # how many sats can you buy with a dollar?
    sats = round(100_000_000 / float(current_price))
    current_price = "{:,}".format(current_price) # add commas

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


@app.route("/repeat-seed")
def repeat_seed():
    codewords = Mnemonic().wordlist
    return render_template("playground/repeat_seed.html", codewords=codewords)


@app.route("/repeat/", methods=["POST", "GET"])
def create_repeat_mnemonic():
    """Create a repeat mnemonic given the repeat word and size."""

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

    return render_template("playground/display_mnemonic_repeat.html", mn_single=phrase, mn_all=mn_all, tot=tot, results=results)


@app.route("/random", methods=["POST", "GET"])
def random(ms=12):
    """Create a random mnemonic phrase."""

    if request.form.get("Select-Size"):
        ms = int(request.form.get("Select-Size"))
        phrase, funded, summary, addr0, results = Wallet.random_wallet(mnemonic_size=ms)

        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        db_entry = Mnemonic_db(mnemonic=phrase, addr0=addr0, funded=funded, summary=summary, datetime=now)
        db.session.add(db_entry)
        db.session.commit()
        return render_template("playground/display_mnemonic_random.html", results=results, phrase=phrase)
    else:
        return render_template("playground/random.html")


@app.route("/brain-wallet/", methods=["GET", "POST"])
def brain_wallet():
    """Create an address from an input string."""

    if request.method == "POST":
        phrase = request.form.get("phrase")
        addr, funded, summary = Wallet.brain_wallet(phrase)
        session[phrase] = [addr, funded, summary]
    return render_template("playground/display_brainwallet.html")


@app.route("/resources")
def resources():
    """Useful bitcoin resources."""
    return render_template("resources.html")


@app.route("/whitepaper")
def whitepaper():
    """Link to the original whitepaper."""
    return redirect("https://bitcoin.org/bitcoin.pdf")


@app.route("/verify-transaction")
def verify_transaction():
    """HTML that describes how transactions are verified."""
    return render_template("learning_lib/verify_transaction.html")


@app.route("/verify-signature")
def verify_signature():
    """HTML that describes how signatures are verified."""
    return render_template("learning_lib/verify_signature.html")


@app.route("/raw-tx")
def raw_tx():
    """HTML that describes the structure of raw transaction."""
    return render_template("learning_lib/transaction_structure.html")


@app.route("/p2sh")
def p2sh():
    """HTML that describes a P2SH tx."""
    return render_template("learning_lib/p2sh.html")


@app.route("/view-db")
def view_db():
    """View the contents of the database that holds mnemonics we have generated."""
    all_mn = Mnemonic_db.query.all()
    return render_template("playground/view_db.html", db=all_mn)


@app.route("/delete-all")
def delete_all():
    """Delete the contents of the database that holds mnemonics we have generated."""
    Mnemonic_db.query.delete()
    db.session.commit()
    return redirect(url_for("view_db"))

@app.route("/clear-session", methods=["POST"])
def clear_session():
    """Delete the contents of the session."""
    session.clear()
    return redirect(url_for("brain_wallet"))


#@app.route("/check-all")
#def check_all():
#    """Generate repeat mnemonics for each of the bip39 code-words."""
#    mn = Mnemonic()
#    wlist = mn.wordlist[:100]
#    for word in wlist:
#        create_repeat_mnemonic(repeat_word=word, mnemonic_size=12)
#    return redirect(url_for("view_db"))
