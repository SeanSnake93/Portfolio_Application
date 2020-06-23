from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
import requests
import os

app = Flask(__name__)

bcrypt = Bcrypt(app)
app.config['SQLALCHEMY_DATABASE_URI'] = str(os.getenv('CROSSWAVE_URI'))
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SECRET_KEY'] = str(os.getenv('STUDIO_KEY')) # Secret Key
db = SQLAlchemy(app)

login_manager = LoginManager(app)
login_manager.login_view = 'login'

from application import routes