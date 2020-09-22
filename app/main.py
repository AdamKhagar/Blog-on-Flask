from flask import Flask, render_template, request
from forms import LoginForm
from secret import secret_key

app = Flask(__name__)
app.debug = True
app.config['SECRET_KEY'] = secret_key

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

if __name__ == '__main__':
    app.run()