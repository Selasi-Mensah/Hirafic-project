#!/usr/bin/env python3
""" This contains the test for the client model """
from flask_sqlalchemy import SQLAlchemy
import pytest
import requests_mock
from flask import Flask
from extensions import db
from models.user import User
from models.client import Client
# Booking needed for initializing mapper
from models.artisan import Artisan
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
    """ works with database """
    with app.app_context():
        # Create tables
        db.create_all()
        # Provide the database object to the test
        yield db
        # Clean up tables after tests
        db.drop_all()


def test_create_client(app: Flask, database: SQLAlchemy):
    """ Test creating a client object """
    with app.app_context():
        # Create a test user to associate with the client
        test_user = User(
            username="Test Client",
            email="client@example.com",
            password="clientpassword",
            phone_number="+1234567890",
            role="Client",
            location="Somewhere",
            created_at=datetime.now(timezone.utc),
            image_file="default.jpeg"
        )
        database.session.add(test_user)
        database.session.commit()

        # Create a test client
        test_client = Client(
            user_id=test_user.id,
            name="Test Client",
            email="client@example.com",
            password="clientpassword",
            phone_number="+1234567890",
            location="Somewhere",
            created_at=datetime.now(timezone.utc)
        )
        database.session.add(test_client)
        database.session.commit()

        # Query the client from the database
        retrieved_client = Client.query.filter_by(name="Test Client").first()

        # Assertions
        assert retrieved_client is not None
        assert retrieved_client.user_id == test_user.id
        assert retrieved_client.name == "Test Client"
        assert retrieved_client.email == "client@example.com"
        assert retrieved_client.phone_number == "+1234567890"
        assert retrieved_client.longitude is None
        assert retrieved_client.latitude is None

        # Test the __repr__ method
        assert repr(retrieved_client) ==\
            "Client('Test Client', 'client@example.com')"
        # Test the dict() method
        assert retrieved_client.to_dict() == {
            'name': 'Test Client',
            'email': 'client@example.com',
            'phone_number': '+1234567890',
            'location': 'Somewhere',
            'latitude': None,
            'longitude': None,
        }


def test_update_client(app: Flask, database: SQLAlchemy):
    """ Test updating client"""
    with app.app_context():
        # Query the client from the database
        client = Client.query.filter_by(name="Test Client").first()
        client.name = "Updated Client"
        client.location = "Updated Location"
        database.session.commit()

        # Query the updated client from the database
        updated_client = Client.query.filter_by(name="Updated Client").first()
        assert updated_client.name == "Updated Client"
        assert updated_client.location == "Updated Location"


def test_delete_client(app: Flask, database: SQLAlchemy):
    """ Test delete cascade, by deleting related user"""
    with app.app_context():
        client = Client.query.filter_by(name="Updated Client").first()
        user = User.query.filter_by(id=client.user_id).first()
        # delete the user from database
        database.session.delete(user)
        database.session.commit()

        # delete cascade deleted the related client too
        deleted_client = Client.query.filter_by(name="Updated Client").first()
        deleted_user = User.query.filter_by(id=client.user_id).first()
        assert deleted_client is None
        assert deleted_user is None


def test_client_validations(app: Flask, database: SQLAlchemy):
    with app.app_context():
        """ Test validatins with creating clients """
        # Test creating a client with a duplicate email
        user1 = User(
            username="client1",
            email="duplicateclient@example.com",
            password="password1",
            phone_number="+1234567890",
            role="Client",
            location="Location 1",
            created_at=datetime.now(timezone.utc),
            image_file="default.jpg"
        )
        database.session.add(user1)
        database.session.commit()

        client1 = Client(
            user_id=user1.id,
            name="client1",
            password="password1",
            email="duplicateclient@example.com",
            phone_number="+1234567890",
            created_at=datetime.now(timezone.utc),
            location="Location 1",
        )
        database.session.add(client1)
        database.session.commit()

        user2 = User(
            username="client2",
            email="duplicateclient@example.com",
            password="password2",
            phone_number="+0987654321",
            role="Client",
            location="Location 2",
            created_at=datetime.now(timezone.utc),
            image_file="default.jpeg"
        )
        database.session.add(user2)
        with pytest.raises(IntegrityError):
            database.session.commit()
        database.session.rollback()

        client2 = Client(
            user_id=user2.id,
            name="Client 2",
            password="password2",
            email="duplicateclient@example.com",
            phone_number="+0987654321",
            created_at=datetime.now(timezone.utc),
            location="Location 2",
        )
        database.session.add(client2)
        with pytest.raises(IntegrityError):
            database.session.commit()
        database.session.rollback()

        # Test creating a client with a missing required field
        user3 = User(
            username="client3",
            email="client3@example.com",
            password="password3",
            phone_number="+1234567890",
            role="Client",
            location="Location 3",
            created_at=datetime.now(timezone.utc),
            image_file="default.jpg"
        )
        client3 = Client(
            user_id=user3.id,
            name=None,  # Name is required
            email="client3@example.com",
            password="password3",
            phone_number="+1234567890",
            location="Location 3"
        )
        database.session.add(user3)
        database.session.add(client3)
        with pytest.raises(IntegrityError):
            database.session.commit()
        database.session.rollback()


def test_geocode_location(app: Flask, database: SQLAlchemy):
    """ Test the artisan geocode location and setting
     the longitude and latitude in the client object """
    with app.app_context():
        # Create a test user
        test_user = User(
            username="geocodeclient",
            email="geocodeclient@example.com",
            password="securepassword",
            phone_number="+1234567890",
            role="Client",
            location="Test Location",
            created_at=datetime.now(timezone.utc),
            image_file="default.jpg"
        )
        database.session.add(test_user)
        database.session.commit()

        # Create a test artisan
        test_artisan = Artisan(
            user_id=test_user.id,
            name="Geocode Client",
            email="geocodeclient@example.com",
            password="securepassword",
            phone_number="+1234567890",
            location="Test Location",
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
    """ Test invalid geocode response for client object"""
    with app.app_context():
        # Create a test user
        test_user = User(
            username="invalidlocclient",
            email="invalidlocclient@example.com",
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
            name="Invalid Location Client",
            email="invalidlocclient@example.com",
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
