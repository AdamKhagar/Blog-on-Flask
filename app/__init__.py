'''app package'''

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import confirm_login



app = Flask(__name__)
app.debug = True
app.config.from_object('config.Config')

db = SQLAlchemy(app)
    
    

from .models import *
db.create_all()

from .utils import is_admin
@app.context_processor
def is_admin_context():
    return dict(is_admin=is_admin)

from . import views