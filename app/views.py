from app import app
from flask import render_template, request
from .forms import LoginForm

@app.route('/')
def main():
    return '<h1>about</h1>'

@app.route('/login/')
def login():
    form = LoginForm()
    if form.validate_on_submit():
        pass
    return render_template('login.html', form=form)

@app.route('/registration/')
def registration():
    pass
