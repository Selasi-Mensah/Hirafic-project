#!/usr/bin/python3
"""Module to run app"""
from __init__ import create_app
from flask import make_response
# from flask import BuildError
# from flask_wtf.csrf import CSRFProtect


app = create_app()
# csrf = CSRFProtect(app)

# @app.errorhandler(BuildError)
# def not_found(error):
#      return make_response(jsonify({'error': 'Not found'}), 404)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5000', debug=True)
