from . import app
from .db import db
from .db.tables import ShortenedURL

from flask import request, abort, make_response, jsonify
from sqlalchemy import select, exists
import string
import random
import html
import datetime

def get_url_or_400() -> str:
    content = request.get_json(force=True)
    if 'url' not in content:
        res = make_response('Error: "url" not in request body')
        res.status_code = 400
        abort(res)
    return content['url']


def generate_code(length: int = 6):
    CODE_CHARS = string.ascii_lowercase + string.digits
    chars = [random.choice(CODE_CHARS) for _ in range(length)]
    return ''.join(chars)

@app.get('/')
def home():
    return ('Hello World')

@app.post('/shorten')
def create_shortened_url():
    url = get_url_or_400()
    while True:
        code = generate_code()
        # Checking if we've already used this
        already_exists = db.session.query(select(ShortenedURL).where(ShortenedURL.code == code).exists()).scalar()
        if not already_exists:
            break

    now = datetime.datetime.now(tz=datetime.UTC)
    shortened = ShortenedURL(code=code, url=url, created_at=now)
    db.session.add(shortened)
    db.session.commit()
    result = {
        'id':       str(shortened.id),
        'url':      url,
        'shortCode':code,
        'createdAt':now.strftime(r"%y-%m-%dT%H:%M:%SZ"),
        'updatedAt':now.strftime(r"%y-%m-%dT%H:%M:%SZ"),
    }

    return jsonify(result), 201

@app.route('/all')
def find_all():
    x = db.session.execute(db.select(ShortenedURL)).scalars()
    return html.escape(str(list(x)))