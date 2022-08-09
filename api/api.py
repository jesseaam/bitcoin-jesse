from flask import Blueprint, jsonify
from application.models import Mnemonic_db, MnSchema


basic_api = Blueprint("basic_api", __name__)
mn_schema = MnSchema(many=True)

@basic_api.route("/")
def api():
    simple_api = "Hello"
    return jsonify(salude=simple_api)


@basic_api.route("/api-not-found")
def api_not_found():
    return jsonify(message="Not found"), 404


@basic_api.route("/btc-or-crypto/<string:response>")
def btc_or_crypto(response: str):
    """btc-or-crypto"""
    
    if response == "crypto":
        return jsonify(message=f"Access denied {response} bro. This is for BTC maximalists only!"), 401
    elif response == "btc":
        return jsonify(message="Access granted. Always happy to host a BTC maximalists!")
    else:
        return jsonify(message=f"<{response}> is not a valid response. Please enter <btc> or <crypto> to enter this site."), 418 # lol

@basic_api.route("/all-mnemonics")
def all_mnemonics():
    all_mn = Mnemonic_db.query.all()
    hi = mn_schema.dump(all_mn)
    return jsonify(hi)
