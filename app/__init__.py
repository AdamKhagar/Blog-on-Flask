from flask import Flask
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.debug = True
app.config.from_object('config.Config')

db = SQLAlchemy(app)
 

from app.models import *

db.create_all()

from app.utils import is_admin
@app.context_processor
def is_admin_context():
    return dict(is_admin=is_admin)

from app import views