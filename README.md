# Implementation of [roadmap.sh - URL Shortening Service](https://roadmap.sh/projects/url-shortening-service)

## Technology: Python3, Flask, SQLite

This project implements the API endpoints as specified in roadmap.sh, and also has a basic
  front-end (for testing) available at the website root.

### How to setup:
1. Ensure [Python 3.12+](https://www.python.org/downloads/) is installed
2. (Optional but recommended)
   1. Create a virtual environment via `$ python -m venv .venv`
   2. Get into this environment using `$ ./.venv/scripts/activate`
3. Install the dependencies via `$ pip install -r requirements.txt`

### How to run:
`$ flask --app ./app/main.py run`