from flask import flash

from app import app
from views import login_manager

@app.error_handler(404)