#!/usr/bin/env python3
"""
This contains test for artisan profile form
"""
from flask_sqlalchemy import SQLAlchemy
import pytest
from flask import Flask
from extensions import db, jwt, redis_client
# The unused models are needed for mapping
from models.user import User
from models.artisan import Artisan
from models.client import Client
from models.booking import Booking
# from forms.auth import RegistrationForm
from forms.artisan import ArtisanProfileForm
from datetime import datetime, timezone


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

    # Create a test client
    client = app.test_client()

    return app


@pytest.fixture(scope="module")
def database(app: Flask):
    """ work wiht database """
    with app.app_context():
        # Create tables
        db.create_all()
        # Provide the database object to the test
        yield db
        # Clean up tables after tests
        db.drop_all()


def test_artisan_profile_form_valid(app: Flask, database: SQLAlchemy):
    """ Testartisan profile form with valid fields """
    with app.app_context():
        user = User(
            username="uniqueuser",
            email="testuser@example.com",
            password="securepassword",
            phone_number="+1234567890",
            role="Client",
            location="Test Location",
            created_at=datetime.now(timezone.utc),
            image_file="default.jpeg",
        )
        database.session.add(user)
        database.session.commit()

        form = ArtisanProfileForm(
            username="Test Artisan",
            email="artisan@example.com",
            phone_number="+1234567890",
            location="Somewhere",
            specialization="Engineering",
            skills="coding",
            picture="default.jpeg",
            submit="True",
        )
        if not form.validate():
            print(form.errors)
        assert form.validate() is True


# def test_artisan_profile_form_invalid_email(app: Flask, database: SQLAlchemy):
#     """ Test artisan profile form with invalid email """
#     with app.app_context():
#         user = User.query.filter_by(username="uniqueuser").first()

#         form = ArtisanProfileForm(
#             username="Test Artisan",
#             email="Invalid email",
#             phone_number="+1234567890",
#             location="Somewhere",
#             specialization="Engineering",
#             skills="coding",
#             picture="default.jpeg",
#             submit="True",
#         )
#         assert not form.validate()
#         assert "Invalid email address." in form.email.errors


# def test_artisan_profile_form_duplicate_username(
#         app: Flask, database: SQLAlchemy):
#     """ Test artisan profile form with duplicate username """
#     with app.app_context():
#         user = User(
#             username="uniqueuser2",
#             email="testuser2@example.com",
#             password="securepassword",
#             phone_number="+1234567890",
#             role="Client",
#             location="Test Location",
#             created_at=datetime.now(timezone.utc),
#             image_file="default.jpeg"
#         )
#         database.session.add(user)
#         database.session.commit()

#         user = User.query.filter_by(username="uniqueuser").first()
#         # update with an already taken username
#         form = ArtisanProfileForm(
#             username="uniqueuser2",
#             email="artisan@example.com",
#             phone_number="+1234567890",
#             location="Somewhere",
#             specialization="Engineering",
#             skills="coding",
#             picture="default.jpeg",
#             submit="True",
#         )
#         assert not form.validate()
#         assert "Username is already taken!" in form.username.errors


# def test_artisan_profile_form_duplicate_email(
#         app: Flask, database: SQLAlchemy):
#     """ Test artisan profile form with duplicate email """
#     with app.app_context():
#         # update with an already taken email
#         user = User.query.filter_by(username="uniqueuser").first()
#         login_user(user)

#         form = ArtisanProfileForm(
#             username="uniqueuser3",
#             email="testuser2@example.com",
#             phone_number="+1234567890",
#             location="Somewhere",
#             specialization="Engineering",
#             skills="coding",
#             picture="default.jpeg",
#             submit="True",
#         )
#         assert not form.validate()
#         assert "Email is already taken!" in form.email.errors


# def test_artian_form_validate_on_submit(app: Flask, database: SQLAlchemy):
#     """ Test artisan form validate_on_submit method """
#     with app.app_context():
#         user = User.query.filter_by(username="uniqueuser").first()
#         login_user(user)
#         with app.test_request_context(method="POST"):
#             form = ArtisanProfileForm(
#                 username="uniqueuser",
#                 email="testuser@example.com",
#                 phone_number="+1234567890",
#                 location="Test Location",
#                 specialization="Engineering",
#                 skills="coding",
#                 picture="default.jpeg",
#                 submit="True",
#             )
#             assert form.validate_on_submit() is True
