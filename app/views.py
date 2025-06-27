import datetime
import html
import random
import string

from flask import abort, jsonify, make_response, request

from . import app
from .db import db
from .db.tables import ShortenedURL


def get_url_or_400() -> str:
    """Helper function
    Grabs the provided URL from the request's JSON body, or aborts with a 400 error"""
    content = request.get_json(force=True)
    if 'url' not in content:
        res = make_response('Error: "url" not in request body')
        res.status_code = 400
        abort(res)
    return content['url']


def generate_code(length: int = 6):
    """
    Generates a random 6-character code
    
    (Note: Might not be unique, check it yourself)
    """
    CODE_CHARS = string.ascii_lowercase + string.digits
    chars = [random.choice(CODE_CHARS) for _ in range(length)]
    return ''.join(chars)

@app.post('/shorten')
def create_short_url():
    """Endpoint.

    Takes a URL and saves a shortened version of it.

    Path:
    - `POST /shorten`

    Request body:
    - JSON with `{'url': <url>}`

    Response:
    - On success:
      - 201: Returns JSON containing:
        - The database entry's ID
        - A unique 6-character identifier for the URL
        - The given URL
        - The UTC datetime for when it was created
        - The UTC datetime for when it was last updated (must be ditto)
    - On failure:
      - 400: If no URL was provided
    """
    url = get_url_or_400()
    while True:
        code = generate_code()
        # Checking if we've already used this
        existing_row = ShortenedURL.find_by_code(code)
        if existing_row is None:
            break

    now = datetime.datetime.now(tz=datetime.UTC)
    shortened = ShortenedURL(code=code, url=url, created_at=now)
    db.session.add(shortened)
    db.session.commit()

    return jsonify(shortened.info_dict()), 201


@app.get('/shorten/<code>')
def retrieve_original_url(code: str):
    """Endpoint.

    Returns the full URL from the given code.

    Path:
    - `GET /shorten/<code>`
      - code: The unique 6-character identifier of the URL

    Output:
    - On success:
      - 200: Returns JSON containing:
        - The database entry's ID
        - A unique 6-character identifier for the URL
        - The given URL
        - The UTC datetime for when it was created
        - The UTC datetime for when it was last updated
    - On failure:
      - 404: If no URL has the given code
    """
    shortened = ShortenedURL.find_by_code_or_404(code)
    shortened.access_count += 1

    db.session.add(shortened)
    db.session.commit()
    
    return jsonify(shortened.info_dict()), 200


@app.put('/shorten/<code>')
def update_short_url(code: str):
    """Endpoint.

    Updates a shortened URL.

    Path:
    - `PUT /shorten/<code>`
      - code: The unique 6-character identifier of the URL

    Request body:
    - JSON with `{'url': <url>}`

    Output:
    - On success:
      - 200: Returns JSON containing:
        - The database entry's ID
        - A unique 6-character identifier for the URL
        - The given URL
        - The UTC datetime for when it was created
        - The UTC datetime for when it was last updated (which was just now)
    - On failure:
      - 400: If no URL was provided
      - 404: If no URL has the given code
    """
    shortened = ShortenedURL.find_by_code_or_404(code)
    url = get_url_or_400()
    shortened.url = url
    shortened.updated_at = datetime.datetime.now(datetime.UTC)

    db.session.add(shortened)
    db.session.commit()

    return jsonify(shortened.info_dict())

@app.delete('/shorten/<code>')
def delete_short_url(code: str):
    """Endpoint.

    Deletes a shortened URL.

    Path:
    - `DELETE /shorten/<code>`
      - code: The unique 6-character identifier of the URL

    Output:
    - On success:
      - 204: Deleted successfully
    - On failure:
      - 404: If no URL has the given code
    """
    shortened = ShortenedURL.find_by_code_or_404(code)
    db.session.delete(shortened)
    return 'Successfully deleted', 204

@app.get('/shortened/<code>/stats')
def get_url_statistics(code: str):
    """Endpoint.

    Returns information about the given shortened URL.

    Path:
    - `GET /shorten/<code>`
      - code: The unique 6-character identifier of the URL

    Output:
    - On success:
      - 200: Returns JSON containing:
        - The database entry's ID
        - A unique 6-character identifier for the URL
        - The given URL
        - The UTC datetime for when it was created
        - The UTC datetime for when it was last updated
        - The number of times this URL has been accessed (`GET /shorten/<code>`)
    - On failure:
      - 404: If no URL has the given code
    """
    shortened = ShortenedURL.find_by_code_or_404(code)
    return shortened.info_dict_full()



@app.route('/all')
def find_all():
    x = db.session.execute(db.select(ShortenedURL)).scalars()
    return html.escape(str(list(x)))
