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
from routes.artisan import artisans_Bp
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
    app.register_blueprint(artisans_Bp)

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
def client(app: Flask):
    return app.test_client()


def test_profile_route_get(client: Any, database: SQLAlchemy):
    """ Test the profile route with GET request """
    # Create and login a user
    response = client.post('/register', data={
        'username': 'testuser',
        'email': 'testuser@example.com',
        'password': 'securepassword',
        'confirm_password': 'securepassword',
        'phone_number': '+1234567890',
        'location': 'Test Location',
        'role': 'Artisan',
    })
    assert response.status_code == 201
    login_response = client.post('/login', data={
        'email': 'testuser@example.com',
        'password': 'securepassword'
    })
    token = login_response.json['access_token']

    # test route without username
    response = client.get('/artisan', headers={
        'Authorization': f'Bearer {token}'
    })
    user = User.query.filter_by(username='testuser').first()
    assert response.status_code == 200
    artisan_data = user.artisan.to_dict()
    artisan_data['image_file'] = user.image_file
    assert response.json == artisan_data

    # test route with username
    response = client.get('/artisan/testuser', headers={
        'Authorization': f'Bearer {token}'
    })
    assert response.status_code == 200

    response = client.get('/logout', headers={
        'Authorization': f'Bearer {token}'
    })


def test_artisan_profile_not_authenticated(
        client: FlaskClient, database: SQLAlchemy):
    """ Test not authenticated user """
    user = User.query.filter_by(username='testuser').first()
    login_response = client.post('/login', data={
        'email': 'testuser@example.com',
        'password': 'securepassword'
    })
    token = login_response.json['access_token']
    # Test when username in route not same as the current_user
    response = client.get('/artisan/test', headers={
        'Authorization': f'Bearer {token}'
    })
    assert response.status_code == 403
    assert response.json['error'] == "User not authenticated"


def test_artisan_profile_for_not_artisan(
        client: FlaskClient, database: SQLAlchemy):
    """ Test current_user role not Artisan"""
    response = client.post('/register', data={
        'username': 'testclient',
        'email': 'testclient@example.com',
        'password': 'securepassword',
        'confirm_password': 'securepassword',
        'phone_number': '+1234567890',
        'location': 'Test Location',
        'role': 'Client',
    })
    assert response.status_code == 201
    login_response = client.post('/login', data={
        'email': 'testclient@example.com',
        'password': 'securepassword'
    })
    token = login_response.json['access_token']

    response = client.get('/artisan', headers={
        'Authorization': f'Bearer {token}'
    })
    assert response.status_code == 403
    assert response.json['error'] == "User is not an artisan"


def test_artisan_profile_post_success(client: Any, database: SQLAlchemy):
    """ Test the artisan profile route with successful post method """
    user = User.query.filter_by(username='testuser').first()
    login_response = client.post('/login', data={
        'email': 'testuser@example.com',
        'password': 'securepassword'
    })
    assert login_response.status_code == 200
    token = login_response.json['access_token']
    response = client.post('/artisan', data={
        'username': user.username,
        'email': user.email,
        'phone_number': user.phone_number,
        'location': user.location,
        'specialization': 'Engineering',
        'skills': 'coding',
        'picture': user.image_file,
        'submit': True
    }, headers={
        'Authorization': f'Bearer {token}'
    })
    print(response.json)
    assert response.status_code == 200
    assert response.is_json
    artisan_data = user.artisan.to_dict()
    assert response.json == artisan_data


def test_artisan_profile_invalid_form(client: Any, database: SQLAlchemy):
    """ Test the artisan profile route with invalid form """
    user = User.query.filter_by(username='testuser').first()
    login_response = client.post('/login', data={
        'email': 'testuser@example.com',
        'password': 'securepassword'
    })
    assert login_response.status_code == 200
    token = login_response.json['access_token']
    response = client.post('/artisan', data={
        # use email for another user
        'email': 'testclient@example.com',
        'phone_number': user.phone_number,
        'location': user.location,
        'specialization': 'Engineering',
        'skills': 'coding',
        'picture': user.image_file,
        'submit': True
    }, headers={
        'Authorization': f'Bearer {token}'
    })

    assert response.status_code == 400
    assert response.is_json
    assert response.json['error'] == "Invalid form data"


def test_artisan_profile_rollback(
        client: FlaskClient, database: SQLAlchemy, app: Flask):
    """ Test the artisan profile route with rollback """
    # Mock internal error
    original_commit = database.session.commit
    try:
        database.session.commit =\
            lambda: (_ for _ in ()).throw(Exception("Simulated failure"))
        user = User.query.filter_by(username='testuser').first()
        login_response = client.post('/login', data={
            'email': 'testuser@example.com',
            'password': 'securepassword'
        })
        assert login_response.status_code == 200
        token = login_response.json['access_token']
        response = client.post('/artisan', data={
            'username': user.username,
            'email': user.email,
            'phone_number': user.phone_number,
            'location': user.location,
            'specialization': 'Engineering',
            'skills': 'coding',
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
