import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask.ext.moment import Moment

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
# Consider pulling in the config from a file instead.
# You can also keep the secret key in a separate file too
app.config[
    'SECRET_KEY'] = b'\x19\xb0\xe5l)\x18\xfb\xfc\x00\xc9"H\x87\x0c\x85\xc7_}\xd0\xa3\xe9\xa5\xb1\x8e\x04\xe8\x1a\x9a\
    x9c\x031\xde'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'thermos.db')
app.config['DEBUG'] = True
#app.config['SERVER_NAME'] = '127.0.0.1:8080'


db = SQLAlchemy(app)

# Configure Authentication
login_manager = LoginManager()
login_manager.session_protection = "strong"
login_manager.login_view = "login"
login_manager.init_app(app)

# for displaying timestamps
moment = Moment(app)

import thermos.models
import thermos.views
