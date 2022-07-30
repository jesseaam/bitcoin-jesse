from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = b"0MjasdL5%37C-111@#" # https://flask.palletsprojects.com/en/1.0.x/quickstart/#sessions


# set up database config
# default postgresql://YOURUSERNAME@localhost/YOURUSERNAME
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://jmarks@localhost/jmarks"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False # adds significant overhead

# create database object
db = SQLAlchemy(app)

from application import routes
