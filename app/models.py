from app import db
from flask_login import UserMixin
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

class UserModel(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    lastname = db.Column(db.String(50))
    username = db.Column(db.String(50), nullable=False, unique=True)
    email = db.Column(db.String(), nullable=False, unique=True)
    password_hash = db.Column(db.String(), nullable=False)
    created_on = db.Column(db.DateTime(), default=datetime.utcnow())

    def __repr__(self):
        '''return '<{}:{}>'.format(self.id, self.username)'''
        return '<{}:{}>'.format(self.id, self.username)

    def set_password(self, password):
        '''generate password hash and set'''
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        '''check password'''
        return check_password_hash(self.password_hash, password)


db.create_all()