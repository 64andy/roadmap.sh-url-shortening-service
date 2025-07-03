from . import app
from .views import *

from flask import send_file

@app.get('/')
def home():
    return send_file('templates/index.html')
