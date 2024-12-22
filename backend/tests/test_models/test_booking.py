import pytest
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
# from models.base import db, Base
# from models.user import User
# from models.client import Client
# from models.artisan import Artisan
# from models.booking import Booking
from __init__ import db, Base, User, Client, Artisan, Booking
from datetime import datetime, timezone


@pytest.fixture(scope="module")
def app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.init_app(app)
    return app


@pytest.fixture(scope="module")
def database(app):
    with app.app_context():
        db.create_all()
        yield db
        db.drop_all()


@pytest.fixture(scope="module")
def user_model():
    """Fixture to provide access to the User model."""
    return User

@pytest.fixture(scope="module")
def client_model():
    """Fixture to provide access to the Client model."""
    return Client


@pytest.fixture(scope="module")
def artisan_model():
    """Fixture to provide access to the Artisan model."""
    return Artisan


@pytest.fixture(scope="module")
def booking_model():
    """Fixture to provide access to the Booking model."""
    return Booking


def test_booking_creation(app, database, user_model, client_model, artisan_model, booking_model):
    with app.app_context():
        # Create a test user for client
        test_client_user = user_model(
            username="testclientuser",
            email="testclient@example.com",
            password="securepassword",
            phone_number="+1234567890",
            role="Client",
            created_at=datetime.now(timezone.utc)
        )
        database.session.add(test_client_user)
        db.session.commit()

        # Create a test client
        test_client = client_model(
            user_id=test_client_user.id,
            name="Test Client",
            email="client@example.com",
            password="clientpassword",
            phone_number="+9876543210",
            created_at=datetime.now(timezone.utc)
        )
        database.session.add(test_client)
        database.session.commit()

        # Create a test user for artisan
        test_artisan_user = user_model(
            username="testartisanuser",
            email="testartisan@example.com",
            password="securepassword",
            phone_number="+1112223333",
            role="Artisan",
            created_at=datetime.now(timezone.utc)
        )
        database.session.add(test_artisan_user)
        database.session.commit()

        # Create a test artisan
        test_artisan = artisan_model(
            user_id=test_artisan_user.id,
            name="Test Artisan",
            email="artisan@example.com",
            password="artisanpassword",
            phone_number="+4445556666",
            location="Test Location",
            Specialization="Engineering",
            skills="Carpentry, Plumbing",
            created_at=datetime.now(timezone.utc)
        )
        database.session.add(test_artisan)
        database.session.commit()

        # Create a test booking
        test_booking = booking_model(
            client_id=test_client.id,
            artisan_id=test_artisan.id,
            status="Pending",
            completion_date=None,
            created_at=datetime.now(timezone.utc)
        )
        database.session.add(test_booking)
        database.session.commit()

        # Query the booking from the database
        retrieved_booking = booking_model.query.first()

        # Assertions
        assert retrieved_booking is not None
        assert retrieved_booking.client_id == test_client.id
        assert retrieved_booking.artisan_id == test_artisan.id
        assert retrieved_booking.status == "Pending"
        assert retrieved_booking.request_date is not None
        assert retrieved_booking.completion_date is None

        # Test the __repr__ method
        #assert repr(retrieved_booking) == f"Booking('{retrieved_booking.id}', 'Pending')"
