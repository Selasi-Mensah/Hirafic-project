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
from extensions import db, login_manager
from flask_login import login_user, logout_user
from models.user import User
# unused models needed for mapping
from models.artisan import Artisan
from models.client import Client
from models.booking import Booking
from routes.client import clients_Bp


@pytest.fixture(scope="module")
def app() -> Flask:
    """ Create a new Flask instance for test """
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["SECRET_KEY"] = "test_secret_key"
    # Disable CSRF for testing
    app.config["WTF_CSRF_ENABLED"] = False

    # Initialize login manager
    login_manager.init_app(app)

    # Define user_loader callback
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Bind SQLAlchemy to the Flask app
    db.init_app(app)

    # Register blueprints
    app.register_blueprint(clients_Bp)

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


def test_client_profile_route_get(client: Any, database: SQLAlchemy):
    """ Test the client profile route with GET request """
    # Create and login a user
    user = User(
        username='testuser',
        email='testuser@example.com',
        password='securepassword',
        phone_number='+1234567890',
        location='Spain',
        role='Client',
    )
    database.session.add(user)
    database.session.commit()
    userclient = Client(
        user_id=user.id,
        name=user.username,
        email=user.email,
        location=user.location,
        password=user.password,
        phone_number=user.phone_number,
    )
    database.session.add(userclient)
    database.session.commit()
    login_user(user)

    # test route without username
    response = client.get('/client')
    assert response.status_code == 200
    client_data = user.client.to_dict()
    client_data['image_file'] = user.image_file
    assert response.json == client_data

    # test route with username
    response = client.get('/client/testuser')
    assert response.status_code == 200

    logout_user()


def test_client_profile_not_authenticated(
        client: FlaskClient, database: SQLAlchemy):
    """ Test not authenticated user """
    user = User.query.filter_by(username='testuser').first()
    login_user(user)
    # Test when username in route not same as the current_user
    response = client.get('/client/test')
    assert response.status_code == 403
    assert response.json['error'] == "User not authenticated"
    logout_user()


def test_client_profile_for_not_client(
        client: FlaskClient, database: SQLAlchemy):
    """ Test current_user role not client user"""
    user = User(
        username='testuser1',
        email='testuser1@example.com',
        password='securepassword',
        phone_number='+1234567890',
        location='Test Location',
        role='Artisan',
    )
    database.session.add(user)
    database.session.commit()
    login_user(user)

    response = client.get('/client')
    assert response.status_code == 403
    assert response.json['error'] == "User is not a client"
    logout_user()


def test_client_profile_post_success(client: Any, database: SQLAlchemy):
    """ Test the client profile route with successful post method """
    user = User.query.filter_by(username='testuser').first()
    login_user(user)
    response = client.post('/client', data={
        'username': user.username,
        'email': user.email,
        'phone_number': user.phone_number,
        'location': user.location,
        'picture': user.image_file,
        'submit': True
    }, follow_redirects=True)
    print(response.json)
    assert response.status_code == 200
    assert response.is_json
    client_data = user.client.to_dict()
    assert response.json == client_data

    logout_user()


def test_client_profile_invalid_form(client: Any, database: SQLAlchemy):
    """ Test the client profile route with invalid form """
    user = User.query.filter_by(username='testuser').first()
    login_user(user)
    response = client.post('/client', data={
        'email': user.email,
        'phone_number': user.phone_number,
        'location': user.location,
        'picture': user.image_file,
        'submit': True
    }, follow_redirects=True)

    assert response.status_code == 400
    assert response.is_json
    # assert response.json['error'] == "Invalid form data"
    logout_user()


def test_client_profile_internal_error(
        client: FlaskClient, database: SQLAlchemy, app: Flask):
    """ Test the client profile route with internal error """
    # Mock internal error
    original_commit = database.session.commit
    try:
        database.session.commit =\
            lambda: (_ for _ in ()).throw(Exception("Simulated failure"))
        user = User.query.filter_by(username='testuser').first()
        login_user(user)
        response = client.post('/client', data={
            'username': user.username,
            'email': user.email,
            'phone_number': user.phone_number,
            'location': user.location,
            'specialization': 'Engineering',
            'skills': 'coding',
            'picture': user.image_file,
            'submit': True
        }, follow_redirects=True)
        assert response.status_code == 400
        assert response.is_json
        # assert response.json['error'] == "An error occurred during updating"
        logout_user()
    finally:
        database.session.commit = original_commit


def test_client_nearby_artisan_not_authenticated(
        client: FlaskClient, database: SQLAlchemy):
    """ Test not authenticated user """
    user = User.query.filter_by(username='testuser').first()
    login_user(user)
    # Test when username in route not same as the current_user
    response = client.get('/client/test/nearby_artisan')
    assert response.status_code == 403
    assert response.json['error'] == "User not authenticated"
    logout_user()


def test_client_nearby_artisan_for_not_client(
        client: FlaskClient, database: SQLAlchemy):
    """ Test current_user role not client user"""
    user = User(
        username='testuser2',
        email='testuser2@example.com',
        password='securepassword',
        phone_number='+1234567890',
        location='Test Location',
        role='Artisan',
    )
    database.session.add(user)
    database.session.commit()
    login_user(user)

    response = client.get('/client/testuser2/nearby_artisan')
    assert response.status_code == 403
    assert response.json['error'] == "User is not a client"
    logout_user()


def test_client_nearby_artisan_success(client: Any, database: SQLAlchemy):
    """ Test success method on client nearby artisan route """
    # create an artisan
    # get the client user and loged in
    user = User.query.filter_by(username='testuser').first()
    login_user(user)
    response = client.get('/client/testuser/nearby_artisan')
    assert response.status_code == 200
    assert response.is_json
    assert isinstance(response.json, list)
    assert all(isinstance(item, dict) for item in response.json)
    required_keys = ['name', 'longitude', 'latitude']
    assert all(
        all(key in item for key in required_keys) for item in response.json)

    logout_user()
