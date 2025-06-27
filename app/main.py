from . import app
from .views import *


@app.get('/')
def home():
    return ('Hello World')
