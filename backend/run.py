#!/usr/bin/env python3
"""Module to run app"""
from __init__ import create_app
from flask import make_response
from os import getenv


app = create_app()
# csrf = CSRFProtect(app)


if __name__ == '__main__':
    host = getenv("API_HOST", "0.0.0.0")
    port = getenv("API_PORT", "5000")
    app.run(host=host, port=port, debug=True)
