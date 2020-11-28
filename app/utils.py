from functools import wraps
from flask import redirect, flash
from flask_login import current_user
from .models import User, Blacklist
from app import app, db


def is_admin():
    return db.session.query(User).filter(
            User.id == current_user.get_id()).first().is_admin

def admin_required(func):
    @wraps(func)
    def decorated_view(*args, **kwargs):
        if is_admin(): 
            return func(*args, **kwargs)
        else:
            flash("You do not have access to this page")
            return redirect('/')
    return decorated_view


def is_not_blocked(func):
    @wraps(func)
    def decorated_view(*args, **kwargs):
        if db.session.query(Blacklist).filter(Blacklist.user_id \
                == current_user.get_id()).count() == 0:
            return func(*args, **kwargs)
        else:
            flash("You've been blocked")
    return decorated_view

