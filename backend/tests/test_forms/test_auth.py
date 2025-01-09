#!/usr/bin/env python3
"""
This contains authentication forms.
Registration and Login forms
"""
from flask_sqlalchemy import SQLAlchemy
import pytest
from flask import Flask
from models.user import User
from models.artisan import Artisan
from models.client import Client
from models.booking import Booking
from forms.auth import RegistrationForm, LoginForm
from extensions import db
from datetime import datetime, timezone


@pytest.fixture(scope="module")
def app() -> Flask:
    """ Create a new Flask instance for test """
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["SECRET_KEY"] = "test_secret_key"
    app.config["WTF_CSRF_ENABLED"] = False  # Disable CSRF for testing
    # Bind SQLAlchemy to the Flask app
    db.init_app(app)
    return app


@pytest.fixture(scope="module")
def database(app: Flask):
    """ work with database """
    with app.app_context():
        # Create tables
        db.create_all()
        # Provide the database object to the test
        yield db
        # Clean up tables after tests
        db.drop_all()


def test_registration_form_valid(app: Flask, database: SQLAlchemy):
    """ test registration form with valid fields """
    with app.app_context():
        form = RegistrationForm(
            username="testuser",
            email="testuser@example.com",
            password="securepassword",
            confirm_password="securepassword",
            phone_number="+1234567890",
            location="Test Location",
            role="Client"
        )
        if not form.validate():
            print(form.errors)
        assert form.validate() is True


def test_registration_form_invalid_email(app: Flask, database: SQLAlchemy):
    """ Test registration form with invalid email"""
    with app.app_context():
        form = RegistrationForm(
            username="testuser",
            email="invalid-email",
            password="securepassword",
            confirm_password="securepassword",
            phone_number="+1234567890",
            location="Test Location",
            role="Client"
        )
        if not form.validate():
            print(form.errors)
        assert "Invalid email address." in form.email.errors


def test_registration_form_password_mismatch(
        app: Flask, database: SQLAlchemy):
    """ Test registration form with mismatch password"""
    with app.app_context():
        form = RegistrationForm(
            username="testuser",
            email="testuser@example.com",
            password="securepassword",
            confirm_password="differentpassword",
            phone_number="+1234567890",
            location="Test Location",
            role="Client"
        )
        if not form.validate():
            print(form.errors)
        assert not form.validate()
        assert "Field must be equal to password." in\
            form.confirm_password.errors


def test_registration_form_duplicate_username(
        app: Flask, database: SQLAlchemy):
    """ Test registration form ith already registered username """
    with app.app_context():
        # Create a user with the same username
        user = User(
            username="testuser",
            email="testuser@example.com",
            password="securepassword",
            phone_number="+1234567890",
            role="Client",
            location="Test Location",
            created_at=datetime.now(timezone.utc),
            image_file="default.jpeg"
        )
        database.session.add(user)
        database.session.commit()

        form = RegistrationForm(
            username="testuser",
            email="newuser@example.com",
            password="securepassword",
            confirm_password="securepassword",
            phone_number="+1234567890",
            location="Test Location",
            role="Client"
        )
        assert form.validate() is False
        assert "Username is already taken!" in form.username.errors


def test_registration_form_duplicate_email(
        app: Flask, database: SQLAlchemy):
    """ Test registration form ith already registered email """
    with app.app_context():
        # Create a user with the same email
        user = User(
            username="uniqueuser",
            email="testuser2@example.com",
            password="securepassword",
            phone_number="+1234567890",
            role="Client",
            location="Test Location",
            created_at=datetime.now(timezone.utc),
            image_file="default.jpeg"
        )
        database.session.add(user)
        database.session.commit()

        form = RegistrationForm(
            username="newuser",
            email="testuser2@example.com",
            password="securepassword",
            confirm_password="securepassword",
            phone_number="+1234567890",
            location="Test Location",
            role="Client"
        )
        assert form.validate() is False
        assert "Email is already taken!" in form.email.errors


def test_login_form_valid(app: Flask, database: SQLAlchemy):
    """ Test login form with valid fields """
    with app.app_context():
        form = LoginForm(
            email="testuser@example.com",
            password="securepassword",
            remember=True
        )
        if not form.validate():
            print(form.errors)
        assert form.validate() is True


def test_login_form_invalid_email(
        app: Flask, database: SQLAlchemy):
    """ Test login form with invalid email """
    with app.app_context():
        form = LoginForm(
            email="invalid-email",
            password="securepassword",
            remember=True
        )
        assert not form.validate()
        assert "Invalid email address." in form.email.errors


def test_login_form_missing_password(app: Flask, database: SQLAlchemy):
    """ Test login form with missing password """
    with app.app_context():
        form = LoginForm(
            email="testuser@example.com",
            password="",
            remember=True
        )
        assert not form.validate()  # Ensure the form validation fails
        assert "This field is required." in form.password.errors
