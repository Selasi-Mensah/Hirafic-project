#!/usr/bin/env python3
""" Contains the error handlers """
from flask import Blueprint, make_response, jsonify


# create handlers blueprint
errors_Bp = Blueprint('errors', __name__)


@errors_Bp.errorhandler(401)
def unauthorized(error) -> str:
    """ Unauthorized handler """
    return jsonify({"error": "Unauthorized"}), 401


@errors_Bp.app_errorhandler(403)
def forbidden(error) -> str:
    """ forbidden handler """
    return make_response(jsonify({'error': 'forbidden'}), 403)


@errors_Bp.app_errorhandler(404)
def not_found(error) -> str:
    """ Not found handler """
    return make_response(jsonify({'error': 'Not found'}), 404)


@errors_Bp.app_errorhandler(500)
def internal_server_error(error) -> str:
    """ Internal server error handler """
    return make_response(jsonify({'error': 'internal_server_error'}), 500)
