#!/usr/bin/python3
from __init__ import create_app
"""Module to run app"""


app = create_app()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5000', debug=True)
