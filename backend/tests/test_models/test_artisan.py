#!/usr/bin/env python3
""" This contains the test for the Artisan model """
from flask_sqlalchemy import SQLAlchemy
import pytest
import requests_mock
from flask import Flask
from extensions import db
from models.user import User
from models.artisan import Artisan
# Booking needed for initializing mapper
from models.booking import Booking
from models.client import Client
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
    """ works with database """
    with app.app_context():
        # Create tables
        db.create_all()
        # Provide the database object to the test
        yield db
        # Clean up tables after tests
        db.drop_all()


def test_create_artisan(app: Flask, database: SQLAlchemy):
    """ Test creating an artisan object """
    with app.app_context():
        # Create a test user to associate with the artisan
        test_user = User(
            username="Test Artisan",
            email="artisan@example.com",
            password="artisanpassword",
            phone_number="+1234567890",
            role="Artisan",
            location="Somewhere",
            created_at=datetime.now(timezone.utc)
        )
        database.session.add(test_user)
        database.session.commit()

        # Create a test artisan
        test_artisan = Artisan(
            user_id=test_user.id,
            name="Test Artisan",
            email="artisan@example.com",
            password="artisanpassword",
            phone_number="+1234567890",
            location="Somewhere",
            specialization="Engineering",
            skills="Carpentry, Plumbing",
            created_at=datetime.now(timezone.utc)
        )
        database.session.add(test_artisan)
        database.session.commit()

        # Query the artisan from the database
        retrieved_artisan =\
            Artisan.query.filter_by(name="Test Artisan").first()

        # Assertions
        assert retrieved_artisan is not None
        assert retrieved_artisan.user_id == test_user.id
        assert retrieved_artisan.name == "Test Artisan"
        assert retrieved_artisan.email == "artisan@example.com"
        assert retrieved_artisan.phone_number == "+1234567890"
        assert retrieved_artisan.location == "Somewhere"
        assert retrieved_artisan.specialization == "Engineering"
        assert retrieved_artisan.skills == "Carpentry, Plumbing"
        assert retrieved_artisan.created_at is not None
        assert retrieved_artisan.longitude is None
        assert retrieved_artisan.latitude is None

        # Test the __repr__ method
        assert repr(retrieved_artisan) ==\
            "Artisan('Test Artisan', 'artisan@example.com, 'Engineering')"

        # Test the dict() method
        assert retrieved_artisan.to_dict() == {
            'username': 'Test Artisan',
            'email': 'artisan@example.com',
            'phone_number': '+1234567890',
            'location': 'Somewhere',
            'image_file': None,
            'bookings': [],
            'latitude': None,
            'longitude': None,
            'id': retrieved_artisan.id,
            'salary_per_hour': 0.0,
            'image_file': '/default.jpeg',
            'specialization': 'Engineering',
            'skills': "Carpentry, Plumbing"
        }


def test_update_artisan(app: Flask, database: SQLAlchemy):
    """ Test updating an artisan object """
    with app.app_context():
        # Query the artisan from the database
        artisan = Artisan.query.filter_by(name="Test Artisan").first()
        artisan.name = "Updated Artisan"
        artisan.location = "Updated Location"
        database.session.commit()

        # Query the updated artisan from the database
        updated_artisan =\
            Artisan.query.filter_by(name="Updated Artisan").first()
        assert updated_artisan.name == "Updated Artisan"
        assert updated_artisan.location == "Updated Location"


def test_delete_artisan(app: Flask, database: SQLAlchemy):
    """ Test delete cascade by deleting the related user"""
    with app.app_context():
        # Query the artisan from the database
        artisan = Artisan.query.filter_by(name="Updated Artisan").first()
        user = User.query.filter_by(id=artisan.user_id).first()
        database.session.delete(user)
        database.session.commit()

        # Query the deleted artisan and user from the database
        deleted_artisan =\
            Artisan.query.filter_by(name="Updated Artisan").first()
        deleted_user = User.query.filter_by(username="Test Artisan").first()
        assert deleted_artisan is None
        assert deleted_user is None


def test_artisan_validations(app: Flask, database: SQLAlchemy):
    """ Test validations with creating an artisan object"""
    with app.app_context():
        # Test creating an artisan with a duplicate email
        user1 = User(
            username="artisan1",
            email="duplicateartisan@example.com",
            password="password1",
            phone_number="+1234567890",
            role="Artisan",
            location="Location 1",
            created_at=datetime.now(timezone.utc),
            image_file="default.jpg"
        )
        database.session.add(user1)
        database.session.commit()

        artisan1 = Artisan(
            user_id=user1.id,
            name="Artisan 1",
            email="duplicateartisan@example.com",
            password="password1",
            phone_number="+1234567890",
            location="Location 1",
            specialization="Specialization 1",
            skills="Skills 1",
            created_at=datetime.now(timezone.utc)
        )
        database.session.add(artisan1)
        database.session.commit()

        user2 = User(
            username="artisan2",
            email="duplicateartisan@example.com",
            password="password2",
            phone_number="+0987654321",
            role="Artisan",
            location="Location 2",
            created_at=datetime.now(timezone.utc),
            image_file="default.jpg"
        )
        database.session.add(user2)
        with pytest.raises(IntegrityError):
            database.session.commit()
        database.session.rollback()

        artisan2 = Artisan(
            user_id=user2.id,
            name="Artisan 2",
            email="duplicateartisan@example.com",
            password="password2",
            phone_number="+0987654321",
            location="Location 2",
            specialization="Specialization 2",
            skills="Skills 2",
            created_at=datetime.now(timezone.utc)
        )

        database.session.add(artisan2)
        with pytest.raises(IntegrityError):
            database.session.commit()
        database.session.rollback()

        # Test creating an artisan with a missing required field
        user3 = User(
            username="artisan3",
            email="artisan3@example.com",
            password="password3",
            phone_number="+1234567890",
            role="Artisan",
            location="Location 3",
            created_at=datetime.now(timezone.utc),
            image_file="default.jpg"
        )
        database.session.add(artisan1)
        database.session.commit()

        artisan3 = Artisan(
            user_id=user3.id,
            name=None,  # Name is required
            email="artisan3@example.com",
            phone_number="+1234567890",
            password="password3",
            location="Location 3",
            specialization="Specialization 3",
            skills="Skills 3",
            created_at=datetime.now(timezone.utc)
        )
        database.session.add(artisan3)
        with pytest.raises(IntegrityError):
            database.session.commit()
        database.session.rollback()


def test_geocode_location(app: Flask, database: SQLAlchemy):
    """ Test the artisan geocode location and setting
     the longitude and latitude in the object """
    with app.app_context():
        # Create a test user
        test_user = User(
            username="geocodeartisan",
            email="geocodeartisan@example.com",
            password="securepassword",
            phone_number="+1234567890",
            role="Artisan",
            location="Test Location",
            created_at=datetime.now(timezone.utc),
            image_file="default.jpg"
        )
        database.session.add(test_user)
        database.session.commit()

        # Create a test artisan
        test_artisan = Artisan(
            user_id=test_user.id,
            name="Geocode Artisan",
            email="geocodeartisan@example.com",
            password="securepassword",
            phone_number="+1234567890",
            location="Test Location",
            specialization="Engineering",
            skills="Test Skills",
            created_at=datetime.now(timezone.utc),
        )
        database.session.add(test_artisan)
        database.session.commit()

        with requests_mock.Mocker() as m:
            m.get("https://nominatim.openstreetmap.org/search", json=[{
                "lat": "12.34",
                "lon": "56.78"
            }])

            test_artisan.geocode_location()
            assert test_artisan.latitude == 12.34
            assert test_artisan.longitude == 56.78


def test_geocode_location_invalid_response(
        app: Flask, database: SQLAlchemy):
    """ Test invalid geocode response for artisan object"""
    with app.app_context():
        # Create a test user
        test_user = User(
            username="invalidlocartisan",
            email="invalidlocartisan@example.com",
            password="securepassword",
            phone_number="+1234567890",
            role="Artisan",
            location="Invalid Location",
            created_at=datetime.now(timezone.utc),
            image_file="default.jpg"
        )
        database.session.add(test_user)
        database.session.commit()

        # Create a test artisan
        test_artisan = Artisan(
            user_id=test_user.id,
            name="Invalid Location Artisan",
            email="invalidlocartisan@example.com",
            password="securepassword",
            phone_number="+1234567890",
            location="Invalid Location",
            specialization="Engineering",
            skills="Test Skills",
            created_at=datetime.now(timezone.utc),
        )
        database.session.add(test_artisan)
        database.session.commit()

        with requests_mock.Mocker() as m:
            m.get("https://nominatim.openstreetmap.org/search", json=[])

            with pytest.raises(
                    ValueError,
                    match="Could not geocode location: Invalid Location"):
                test_artisan.geocode_location()
