from app import app, db
from flask import render_template, request, redirect, url_for, flash
from flask_login import LoginManager, login_required, login_user, current_user, logout_user
from .models import UserModel
from .forms import LoginForm, RegisterForm
import json

login_manager = LoginManager(app)

@login_manager.user_loader
def load_user(user_id):
    return db.session.query(UserModel).get(user_id)

@app.route('/')
@app.route('/main/')
@login_required
def main():
    return '<h1>about</h1>'

@app.route('/login/', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit() and request.method == 'POST':
        user = db.session.query(UserModel).filter(UserModel.username == form.username.data ).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember.data)
            return redirect(url_for('main'))
        
        flash('Invalid username/password', 'error')
        return redirect(url_for('login'))
        
    return render_template('login.html', title='Login', form=form)

@app.route('/register/', methods=['GET', 'POST'])
def registration():
    form = RegisterForm()
    if form.validate_on_submit() and request.method == 'POST':
        user = UserModel()
        user.name = form.name.data
        if len(form.lastname.data) > 0:
            user.lastname = form.lastname.data
        user.username = form.username.data
        user.email = form.email.data
        user.set_password(form.password.data)
        
        db.session.add_all([user])
        db.session.commit()

        redirect(url_for('main'))

        login_user(user, remember=form.remember.data)

    return render_template('login.html',title='Register', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("You have been logged out.")
    return redirect(url_for('login'))