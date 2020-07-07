from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
import requests
import os

app = Flask(__name__)

from application import routes