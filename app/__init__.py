'''app package'''

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.debug = True
app.config.from_object('config.Config')

db = SQLAlchemy(app)

from .models import *
db.create_all()

from . import views