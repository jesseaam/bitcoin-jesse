from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

app = Flask(__name__)
app.secret_key = b"0MjasdL5%39997C-111@#" # https://flask.palletsprojects.com/en/1.0.x/quickstart/#sessions


# set up database config
# default postgresql://YOURUSERNAME@localhost/YOURUSERNAME
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://jmarks@localhost/jmarks"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False # adds significant overhead


db = SQLAlchemy(app) # create database object
ma = Marshmallow(app)


from application import routes
from application import command_line_tools
