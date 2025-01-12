#!/usr/bin/env python3
"""
This contais tests for artisan routes
"""
from datetime import datetime, timezone
from typing import Any
from flask.testing import FlaskClient
from flask_sqlalchemy import SQLAlchemy
import pytest
from flask import Flask
from extensions import db, jwt, redis_client
from models.user import User
# unused models needed for mapping
from models.artisan import Artisan
from models.client import Client
from models.booking import Booking
from routes.client import clients_Bp
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
    app.register_blueprint(clients_Bp)

    # Create a test client
    client = app.test_client()

    return app


@pytest.fixture(scope="module")
def database(app: Flask):
    with app.app_context():
        # Create tables
        db.create_all()
        # Provide the database object to the test
        yield db
        # Clean up tables after tests
        db.drop_all()


@pytest.fixture(scope="module")
def database(app: Flask):
    with app.app_context():
        # Create tables
        db.create_all()
        # Provide the database object to the test
        yield db
        # Clean up tables after tests
        db.drop_all()


@pytest.fixture(scope="module")
def client(app: Flask):
    return app.test_client()


def test_client_profile_route_get(client: Any, database: SQLAlchemy):
    """ Test the client profile route with GET request """
    # Create and login a user
    response = client.post('/register', data={
        'username': 'testuser',
        'email': 'testuser@example.com',
        'password': 'securepassword',
        'confirm_password': 'securepassword',
        'phone_number': '+1234567890',
        'location': 'Test Location',
        'role': 'Client',
    })
    assert response.status_code == 201
    login_response = client.post('/login', data={
        'email': 'testuser@example.com',
        'password': 'securepassword'
    })
    assert login_response.status_code == 200
    token = login_response.json['access_token']

    # test route without username
    response = client.get('/client', headers={
        'Authorization': f'Bearer {token}'
    })
    assert response.status_code == 200
    user = User.query.filter_by(username='testuser').first()
    client_data = user.client.to_dict()
    client_data['image_file'] = user.image_file
    assert response.json == client_data

    # test route with username
    response = client.get('/client/testuser', headers={
        'Authorization': f'Bearer {token}'
    })
    assert response.status_code == 200
    assert response.json == client_data


def test_client_profile_not_authenticated(
        client: FlaskClient, database: SQLAlchemy):
    """ Test not authenticated user """
    user = User.query.filter_by(username='testuser').first()
    login_response = client.post('/login', data={
        'email': 'testuser@example.com',
        'password': 'securepassword'  # not hashed
    })
    assert login_response.status_code == 200
    token = login_response.json['access_token']
    # Test when username in route not same as the current_user
    response = client.get('/client/test', headers={
        'Authorization': f'Bearer {token}'
    })
    assert response.status_code == 403
    assert response.json['error'] == "User not authenticated"


def test_client_profile_for_not_client(
        client: FlaskClient, database: SQLAlchemy):
    """ Test current_user role not client user"""
    response = client.post('/register', data={
        'username': 'testartisan',
        'email': 'testartisan@example.com',
        'password': 'securepassword',
        'confirm_password': 'securepassword',
        'phone_number': '+1234567890',
        'location': 'Test Location',
        'role': 'Artisan',
    })
    assert response.status_code == 201
    login_response = client.post('/login', data={
        'email': 'testartisan@example.com',
        'password': 'securepassword'
    })
    assert login_response.status_code == 200
    token = login_response.json['access_token']

    response = client.get('/client', headers={
        'Authorization': f'Bearer {token}'
    })
    assert response.status_code == 403
    assert response.json['error'] == "User is not a client"


def test_client_profile_post_success(client: Any, database: SQLAlchemy):
    """ Test the client profile route with successful post method """
    login_response = client.post('/login', data={
        'email': 'testuser@example.com',
        'password': 'securepassword'
    })
    assert login_response.status_code == 200
    token = login_response.json['access_token']
    user = User.query.filter_by(username='testuser').first()
    response = client.post('/client', data={
        'username': 'clienttest',
        'email': 'testuser@example.com',
        'phone_number': '01234567890',
        'location': 'Sudan',
        'picture': 'default.jpg',
        'submit': True
    }, headers={
        'Authorization': f'Bearer {token}'
    })
    assert response.status_code == 200
    assert response.is_json
    user = User.query.filter_by(username='clienttest').first()
    client_data = user.client.to_dict()
    assert response.json == client_data


def test_client_profile_invalid_form(client: Any, database: SQLAlchemy):
    """ Test the client profile route with invalid form """
    response = client.post('/register', data={
        'username': 'testinvalid',
        'email': 'testinvalid@example.com',
        'password': 'securepassword',
        'confirm_password': 'securepassword',
        'phone_number': '+1234567890',
        'location': 'Sudan',
        'role': 'Client',
    })
    assert response.status_code == 201
    login_response = client.post('/login', data={
        'email': 'testuser@example.com',
        'password': 'securepassword'
    })
    assert login_response.status_code == 200
    token = login_response.json['access_token']
    user = User.query.filter_by(username='testinvalid').first()
    response = client.post('/client', data={
        # use email for another user
        'email': user.email,
        'phone_number': user.phone_number,
        'location': user.location,
        'picture': user.image_file,
        'submit': True
    }, headers={
        'Authorization': f'Bearer {token}'
    })

    assert response.status_code == 400
    assert response.is_json
    assert response.json['error'] == "Invalid form data"


def test_client_profile_internal_error(
        client: FlaskClient, database: SQLAlchemy, app: Flask):
    """ Test the client profile route with internal error """
    # Mock internal error
    original_commit = database.session.commit
    try:
        database.session.commit =\
            lambda: (_ for _ in ()).throw(Exception("Simulated failure"))
        login_response = client.post('/login', data={
            'email': 'testuser@example.com',
            'password': 'securepassword'
        })
        assert login_response.status_code == 200
        token = login_response.json['access_token']
        user = User.query.filter_by(username='clienttest').first()
        response = client.post('/client', data={
            'username': user.username,
            'email': user.email,
            'phone_number': user.phone_number,
            'location': user.location,
            'picture': user.image_file,
            'submit': True
        }, headers={
            'Authorization': f'Bearer {token}'
        })
        assert response.status_code == 400
        assert response.is_json
        assert response.json['error'] == "An error occurred during updating"
    finally:
        database.session.commit = original_commit


def test_client_nearby_artisan_not_authenticated(
        client: FlaskClient, database: SQLAlchemy):
    """ Test not authenticated user """
    user = User.query.filter_by(username='clienttest').first()
    login_response = client.post('/login', data={
        'email': 'testuser@example.com',
        'password': 'securepassword'
        })
    assert login_response.status_code == 200
    token = login_response.json['access_token']
    # Test when username in route not same as the current_user
    response = client.get('/client/test/nearby_artisan', headers={
        'Authorization': f'Bearer {token}'
    })
    assert response.status_code == 403
    assert response.json['error'] == "User not authenticated"


def test_client_nearby_artisan_for_not_client(
        client: FlaskClient, database: SQLAlchemy):
    """ Test current_user role not client user"""
    user = User.query.filter_by(username='testartisan').first()
    login_response = client.post('/login', data={
        'email': 'testartisan@example.com',
        'password': 'securepassword'
    })
    assert login_response.status_code == 200
    token = login_response.json['access_token']
    response = client.get('/client/testartisan/nearby_artisan', headers={
        'Authorization': f'Bearer {token}'
    })
    assert response.status_code == 403
    assert response.json['error'] == "User is not a client"


def test_client_nearby_artisan_success(client: Any, database: SQLAlchemy):
    """ Test success method on client nearby artisan route """
    # create an artisan
    # get the client user and loged in
    user = User.query.filter_by(username='testuser').first()
    login_response = client.post('/login', data={
        'email': 'testuser@example.com',
        'password': 'securepassword'
    })
    assert login_response.status_code == 200
    token = login_response.json['access_token']
    response = client.get('/client/clienttest/nearby_artisan',
                          headers={'Authorization': f'Bearer {token}'})
    print(response.json)
    assert response.status_code == 200
    assert response.is_json
    assert isinstance(response.json, list)
    assert all(isinstance(item, dict) for item in response.json)
    required_keys = ['name', 'longitude', 'latitude']
    assert all(
        all(key in item for key in required_keys) for item in response.json)
