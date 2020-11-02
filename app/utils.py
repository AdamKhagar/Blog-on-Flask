from functools import wraps
from flask import redirect, flash
from flask_login import current_user
from .models import User
from app import app, db



def is_admin():
    return db.session.query(User.is_admin).filter(
            User.id == current_user.get_id()).first()[0]

def admin_required(func):
    @wraps(func)
    def decorated_view(*args, **kwargs):
        if is_admin(): 
            return func(*args, **kwargs)
        else:
            flash("You do not have access to this page")
            return redirect('/')
    return decorated_view


