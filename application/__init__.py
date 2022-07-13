from flask import Flask

app = Flask(__name__)
app.secret_key = b'0MjasdL5%37C-111@#' # https://flask.palletsprojects.com/en/1.0.x/quickstart/#sessions


from application import routes
