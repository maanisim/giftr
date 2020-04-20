from flask import Flask
from flask_mysqldb import MySQL
import os

app = Flask(__name__)
app.config.from_pyfile('config.py')
app.secret_key = os.urandom(24)

mysql = MySQL(app)

from giftr import routes