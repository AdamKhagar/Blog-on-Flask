from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, SubmitField, PasswordField
from wtforms.validators import DataRequired, Email, length, EqualTo

class LoginForm(FlaskForm):
    username = StringField(render_kw={'placeholder': 'Username'}, validators=[DataRequired()])
    password = PasswordField(render_kw={'placeholder': 'Password'}, validators=[DataRequired()])
    remember = BooleanField('Remember me')

class RegisterForm(FlaskForm):
    name = StringField(validators=[DataRequired(), length(max=20)], render_kw={'placeholder': 'Name'})
    lastname = StringField(validators=[length(max=20)], render_kw={'placeholder': 'Lastname'})
    username = StringField(validators=[DataRequired(), length(max=20)], render_kw={'placeholder': 'Username'})
    email = StringField(validators=[DataRequired(), Email()], render_kw={'type': 'email', 'placeholder': 'Email'})
    password = PasswordField(validators=[
        DataRequired(),
        length(min=8, max=20),
        EqualTo('confirm', message='Passwords must be the same')], 
        render_kw={'placeholder': 'Password'}
    )
    confirm = PasswordField(render_kw={'placeholder': 'Password again'})
    remember = BooleanField('Remember me')
    agree = BooleanField('I agree to the terms of the license agreement')