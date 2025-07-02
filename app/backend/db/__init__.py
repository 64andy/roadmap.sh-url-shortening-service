from .. import app

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    pass

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///url_shortener.db'
db = SQLAlchemy(app, model_class=Base)

# Import the relevant classes
from .tables import ShortenedURL

with app.app_context():
    db.create_all()
