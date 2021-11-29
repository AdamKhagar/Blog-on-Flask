from logging import DEBUG
import os

app_dir = os.path.abspath(os.path.dirname(__file__))

class Config:
    DEBUG = True
    SECRET_KEY = 'A SECRET KEY'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = "sqlite:///db.sqlite3"