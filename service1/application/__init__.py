from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
import requests
import os

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = str(os.getenv('CROSSWAVE_URI')) # Access point
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SECRET_KEY'] = str(os.getenv('STUDIO_KEY')) # Secret Key
db = SQLAlchemy(app)

from application import routes