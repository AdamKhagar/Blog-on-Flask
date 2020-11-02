from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, SubmitField, PasswordField, SelectField, TextAreaField
from wtforms.validators import DataRequired, Email, length, EqualTo
from app import db
from .models import Category


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember me', render_kw={'label': 'Remember Me'})
#     submit = SubmitField('', render_kw={'value': 'Log In'})


class RegisterForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), length(max=20)])
    lastname = StringField('Lastname', validators=[length(max=20)])
    username = StringField('Username', validators=[DataRequired(), 
            length(min=4, max=20)]
    )
    email = StringField('Email', validators=[DataRequired(), Email()],
            render_kw={'type': 'email'}
    )
    password = PasswordField('Password', validators=[DataRequired(),
            length(min=8, max=20), 
            EqualTo('confirm', message='Passwords must be the same')]
    )
    confirm = PasswordField('Password again')
    remember = BooleanField('Remember me')
#     submit = SubmitField('', render_kw={'value': 'Sign Up'})


class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), length(max=255)],
            render_kw={'autocomplete':'off'}
    )
    tags = StringField('Tags', render_kw={'autocomplete': 'off'})
    category = SelectField('Category', validators=[DataRequired()],
            choices=Category.get_list()
    )
    preview_text = TextAreaField('Preview text', validators=[DataRequired()],
            render_kw={'resize': 'none', 'wrap': 'soft', 'autocomplete': 'off',
                    'maxlength': '1000', 'class': 'prev'}
    )
    text = TextAreaField('Post text', validators=[DataRequired()],
            render_kw={'resize': 'none', 'wrap': 'soft', 'autocomplete': 'off',
                    'class': 'content'}
    )
    submit = SubmitField('', render_kw={'value': 'Post'})