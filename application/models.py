from application import app, db, ma
from sqlalchemy import Column, String, Integer

class Mnemonic_db(db.Model):
    __tablename__="mn"
    id = Column(Integer, primary_key=True) # automatically incremented by db
    mnemonic = Column(String) # unique=True
    addr0 = Column(String)
    funded = Column(Integer)
    summary = Column(Integer)
    datetime = Column(String)

    def __init__(self,mnemonic,addr0,funded,summary,datetime):
        self.mnemonic = mnemonic
        self.addr0 = addr0
        self.funded = funded
        self.summary = summary
        self.datetime = datetime


# Marshmallow - serialize object so we can return JSON
class MnSchema(ma.Schema):
    class Meta():
        fields = ("mnemonic", "addr0", "funded", "summary")
