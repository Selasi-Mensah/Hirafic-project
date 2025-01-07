#!/usr/bin/env python3
"""
Contains tests for the error handlers
"""
from typing import Any
from flask.testing import FlaskClient
import pytest
from flask import Flask, abort
from extensions import db
from routes.handlers import errors_Bp as errors_blueprint


@pytest.fixture(scope="module")
def app() -> Flask:
    """ Create a new Flask instance for test """
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["SECRET_KEY"] = "test_secret_key"

    # Bind SQLAlchemy to the Flask app
    db.init_app(app)

    # Register blueprints
    app.register_blueprint(errors_blueprint)

    @app.route('/forbidden')
    def forbidden_route():
        abort(403)

    @app.route('/error')
    def error_route():
        raise Exception("Test exception")

    @app.route('/unauthorized')
    def unauthorized_route():
        abort(401)

    return app


@pytest.fixture(scope="module")
def client(app: Flask):
    return app.test_client()


def test_forbidden_handler(client: Any):
    """ Test the forbidden error handler """
    response = client.get('/forbidden')
    assert response.status_code == 403
    assert response.is_json
    assert response.json['error'] == 'forbidden'


def test_not_found_handler(client: FlaskClient):
    """ Test the not found error handler """
    response = client.get('/nonexistent_route')
    assert response.status_code == 404
    assert response.is_json
    assert response.json['error'] == 'Not found'


def test_internal_server_error_handler(client: FlaskClient):
    """ Test the internal server error handler """
    response = client.get('/error')
    assert response.status_code == 500
    assert response.is_json
    assert response.json['error'] == 'internal_server_error'


def test_unauthorized_handler(client: FlaskClient):
    """ Test the unauthorized error handler """
    response = client.get('/unauthorized')
    assert response.status_code == 401
    assert response.is_json
    assert response.json['error'] == 'Unauthorized'
