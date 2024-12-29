#!/usr/bin/python3
"""Module to run app"""
from __init__ import create_app
from flask import make_response


app = create_app()


# @app.errorhandler(404)
# def not_found(error):
#      return make_response(jsonify({'error': 'Not found'}), 404)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5000', debug=True)
