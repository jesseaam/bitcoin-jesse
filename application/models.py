from application import app, db

#class Mnemonic_db(db.Model):
#    __tablename__="jmarks"
#    id = db.Column(db.Integer, primary_key=True) # automatically incremented by db
#    test1 = db.Column(db.Integer) # unique=True
#    test2 = db.Column(db.String(40))
#
#    def __init__(self,test1,test2):
#        self.test1=test1
#        self.test2=test2

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