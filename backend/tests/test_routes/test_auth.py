#!/usr/bin/env python3
"""
This contains tests for the authentication:
    - Registration
    - login
    - logout
"""
import warnings
from flask.testing import FlaskClient
import pytest
from flask import Flask
from typing import Any
from flask_sqlalchemy import SQLAlchemy
from extensions import db, jwt, redis_client
from models.user import User
# unused import for models is needed for mapping
from models.artisan import Artisan
from models.client import Client
from models.booking import Booking
from routes.auth import users_Bp


@pytest.fixture(scope="module")
def app() -> Flask:
    """ Create a new Flask instance for test """
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["SECRET_KEY"] = "test_secret_key"
    # Disable CSRF for testing
    app.config["WTF_CSRF_ENABLED"] = False
    app.config["JWT_VERIFY_SUB"] = False

    # Bind SQLAlchemy to the Flask app
    db.init_app(app)
    # Initialize JWT
    jwt.init_app(app)
    # Initialize redis
    redis_client.init_app(app)

    # Register blueprints
    app.register_blueprint(users_Bp)

    # Create a test client
    client = app.test_client()

    return app


@pytest.fixture(scope="module")
def database(app: Flask):
    """ Work with database """
    with app.app_context():
        # Create tables
        db.create_all()
        # Provide the database object to the test
        yield db
        # Clean up tables after tests
        db.drop_all()


@pytest.fixture(scope="module")
def client(app: Flask):
    # Create a test client using the Flask application
    return app.test_client()


def test_register_get(client: Any, database: SQLAlchemy):
    """ Test the register route with get method """
    response = client.get('/register')
    assert response.status_code == 200
    assert response.is_json is True
    expected_fields = ['fields_to_submit']
    actual_fields = response.json.keys()
    assert sorted(expected_fields) == sorted(actual_fields)


def test_register_post_success(client: Any, database: SQLAlchemy):
    """ Test the register route with successful post method """
    response = client.post('/register', data={
        'username': 'testuser',
        'email': 'testuser@example.com',
        'password': 'securepassword',
        'confirm_password': 'securepassword',
        'phone_number': '+1234567890',
        'location': 'Test Location',
        'role': 'Client',
    }, follow_redirects=True)
    assert response.status_code == 201
    assert response.is_json
    assert all(key in response.json for key in [
        'username', 'email', 'phone_number', 'location'])


def test_register_post_authenticated(
        client: FlaskClient, database: SQLAlchemy):
    """ Mock authenticated user """
    response = client.post('/register', data={
        'username': 'testoken',
        'email': 'testoken@example.com',
        'password': 'securepassword',
        'confirm_password': 'securepassword',
        'phone_number': '+1234567890',
        'location': 'Test Location',
        'role': 'Client',
    }, follow_redirects=True)
    login_response = client.post('/login', data={
        'email': 'testoken@example.com',
        'password': 'securepassword',
    })
    token = login_response.json['access_token']
    response = client.get('/register', headers={
        'Authorization': f'Bearer {token}'
    })
    assert response.status_code == 400
    assert response.is_json
    assert response.json['error'] == "User already Loged in"


def test_register_post_validation_error(
        client: FlaskClient, database: SQLAlchemy):
    data = {
        'username': '',
        'email': 'invalid',
        'phone_number': '+1234567890',
        'location': ''
    }
    response = client.post('/register', json=data)
    assert response.status_code == 400
    assert response.is_json
    assert response.json['error']['email'] == ['Invalid email address.']


def test_register_post_internal_error(
        client: FlaskClient, database: SQLAlchemy, app: Flask):
    """ Test the register route with internal error """
    # Mock internal error
    original_commit = database.session.commit
    try:
        database.session.commit =\
            lambda: (_ for _ in ()).throw(Exception("Simulated failure"))
        response = client.post('/register', data={
            'username': 'testuser3',
            'email': 'testuser3@example.com',
            'password': 'securepassword',
            'confirm_password': 'securepassword',
            'phone_number': '+1234567890',
            'location': 'Test Location',
            'role': 'Client',
        }, follow_redirects=True)
        assert response.status_code == 500
        assert response.is_json
        assert response.json['error'] == "Unable to complete registration"
    finally:
        database.session.commit = original_commit


def test_login_get(client: Any, database: SQLAlchemy):
    """ Test the login route with get method """
    response = client.get('/login')
    assert response.status_code == 200
    assert response.is_json is True
    expected_fields = ['fields_to_submit']
    actual_fields = response.json.keys()
    assert sorted(expected_fields) == sorted(actual_fields)
    assert response.json ==\
        {"fields_to_submit": "email, password, remember, submit"}


def test_login_post_success(client: Any, database: SQLAlchemy):
    """ Test the login route with successful post method """
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", DeprecationWarning)
        response = client.post('/login', data={
            'email': 'testuser@example.com',
            'password': 'securepassword',
            'remember': True,
            'submit': True,
        }, follow_redirects=True)
        assert response.status_code == 200
        assert response.is_json


def test_login_post_authenticated(
        client: FlaskClient, database: SQLAlchemy):
    """ Mock authenticated user """
    user = User.query.filter_by(username='testuser').first()
    login_response = client.post('/login', data={
        'email': 'testuser@example.com',
        'password': 'securepassword',
    })
    token = login_response.json['access_token']
    response = client.get('/login', headers={
        'Authorization': f'Bearer {token}'
    })
    assert response.status_code == 400
    assert response.is_json
    assert response.json['error'] == "User already Loged in"
    response = client.get('/logout')


def test_login_post_validation_error(
        client: FlaskClient, database: SQLAlchemy):
    """ Test login route with validation error """
    # Test invalid form
    data = {
        'email': '',
        'email': 'invalid',
        'phone_number': '+1234567890',
        'location': ''
    }
    response = client.post('/login', json=data)
    assert response.status_code == 400
    assert response.is_json
    assert response.json['error'] == "Invalid form data"

    # test invalid username or invalid password
    data = {
        'email': 'testuser@example.com',
        # invalid password
        'password': 'password',
        'remember': True,
        'submit': True
    }
    response = client.post('/login', json=data)
    assert response.status_code == 400
    assert response.is_json
    assert response.json['error'] == "Invalid email or password"


def test_logout_get(client: Any, database: SQLAlchemy):
    """ Test the login route with get method """
    # Test no user is loged in (not authenticated)
    response = client.get('/logout', headers={
        'Authorization': 'something'
    })
    assert response.status_code == 401
    assert response.json['msg'] == "Missing 'Bearer' type in 'Authorization'"\
        " header. Expected 'Authorization: Bearer <JWT>'"

    # Test successful logout
    user = User.query.filter_by(username='testuser').first()
    login_response = client.post('/login', data={
        'email': "testuser@example.com",
        'password': 'securepassword',
    })
    token = login_response.json['access_token']
    response = client.get('/logout', headers={
        'content-type': 'application/json',
        'Authorization': f'Bearer {token}'
    })
    assert response.status_code == 200
    assert response.is_json is True
    assert response.json['message'] == "User logged out"
