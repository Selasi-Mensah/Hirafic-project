#!/usr/bin/env python
""" This contains the test for the user model """
from flask_sqlalchemy import SQLAlchemy
import pytest
from flask import Flask
from extensions import db
from models.user import User
# Client and Booking needed for initializing mapper
from models.client import Client
from models.booking import Booking
from datetime import datetime, timezone
from sqlalchemy.exc import IntegrityError


@pytest.fixture(scope="module")
def app() -> Flask:
    """ Create a new Flask instance for test """
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["SECRET_KEY"] = "test_secret_key"
    # Bind SQLAlchemy to the Flask app
    db.init_app(app)
    return app


@pytest.fixture(scope="module")
def database(app: Flask):
    """ work with database """
    with app.app_context():
        # Create tables in the database
        db.create_all()
        # Provide the database object to the test
        yield db
        # Drop all tables after the test
        db.drop_all()


def test_create_user(app: Flask, database: SQLAlchemy):
    """ Test creating a user object """
    with app.app_context():
        # Create a test user
        test_user = User(
            username="testuser",
            email="testuser@example.com",
            password="securepassword",
            phone_number="+1234567890",
            role="Client",
            location="Somewhere",
            created_at=datetime.now(timezone.utc),
            image_file="default.jpeg"
        )
        database.session.add(test_user)
        database.session.commit()

        # Query the user from the database
        retrieved_user = User.query.filter_by(username="testuser").first()

        # Assertions
        assert retrieved_user is not None
        assert retrieved_user.username == "testuser"
        assert retrieved_user.email == "testuser@example.com"
        assert retrieved_user.phone_number == "+1234567890"
        assert retrieved_user.role == "Client"
        assert retrieved_user.location == "Somewhere"
        assert retrieved_user.created_at is not None
        assert retrieved_user.image_file == "default.jpeg"

        # Test the __repr__ method
        assert repr(retrieved_user) ==\
            "User('testuser', 'testuser@example.com')"
        # Test the to_dict method
        assert retrieved_user.to_dict() == {
            'id': retrieved_user.id,
            'image_file': '/default.jpeg',
            'username': 'testuser',
            'email': 'testuser@example.com',
            'phone_number': '+1234567890',
            'role': 'Client',
            'location': 'Somewhere'
        }


def test_update_user(app: Flask, database: SQLAlchemy):
    """ Test updating a user object """
    with app.app_context():
        # Query the user from the database
        user = User.query.filter_by(username="testuser").first()
        user.username = "updateduser"
        user.location = "nowhere"
        database.session.commit()

        # Query the updated user from the database
        updated_user = User.query.filter_by(username="updateduser").first()
        assert updated_user.username == "updateduser"
        assert updated_user.location == "nowhere"


def test_delete_user(app: Flask, database: SQLAlchemy):
    """ Test deleting a user object """
    with app.app_context():
        # Query the user from the database
        user = User.query.filter_by(username="updateduser").first()
        database.session.delete(user)
        database.session.commit()

        # Query the deleted user from the database
        deleted_user = User.query.filter_by(username="updateduser").first()
        assert deleted_user is None


def test_user_validations(app: Flask, database: SQLAlchemy):
    """ Test validation for user objects """
    with app.app_context():
        # Test creating a user with a duplicate email
        user1 = User(
            username="user1",
            email="duplicate@example.com",
            password="password1",
            phone_number="+1234567890",
            role="Client",
            location="Somewhere",
            created_at=datetime.now(timezone.utc),
            image_file="default.jpg"
        )
        user2 = User(
            username="user2",
            email="duplicate@example.com",
            password="password2",
            phone_number="+0987654321",
            role="Client",
            location="Somewhere",
            created_at=datetime.now(timezone.utc),
            image_file="default.jpeg"
        )
        database.session.add(user1)
        database.session.commit()

        database.session.add(user2)
        with pytest.raises(IntegrityError):
            database.session.commit()
        database.session.rollback()

        # Test creating a user with a missing required field
        user3 = User(
            username="user3",
            email=None,  # Email is required
            password="password3",
            phone_number="+1234567890",
            role="Client",
            location="Somewhere",
            created_at=datetime.now(timezone.utc),
            image_file="default.jpeg"
        )
        database.session.add(user3)
        with pytest.raises(IntegrityError):
            database.session.commit()
        database.session.rollback()
