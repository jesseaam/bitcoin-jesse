from application import app, db

class Mnemonic_db(db.Model):
    __tablename__="mn"
    id = db.Column(db.Integer, primary_key=True) # automatically incremented by db
    mnemonic = db.Column(db.String) # unique=True
    addr0 = db.Column(db.String)
    funded = db.Column(db.Integer)
    summary = db.Column(db.Integer)
    datetime = db.Column(db.String)

    def __init__(self,mnemonic,addr0,funded,summary,datetime):
        self.mnemonic = mnemonic
        self.addr0 = addr0
        self.funded = funded
        self.summary = summary
        self.datetime = datetime


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