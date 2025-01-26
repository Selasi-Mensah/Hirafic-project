import pytest
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from extensions import db
from models.user import User
from models.client import Client
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


def test_booking_creation(app: Flask, database: SQLAlchemy):
    with app.app_context():
        # Create a test user for client
        test_client_user = User(
            username="testclientuser",
            email="testclient@example.com",
            password="securepassword",
            location="Somewhere",
            phone_number="+1234567890",
            role="Client",
            created_at=datetime.now(timezone.utc)
        )
        database.session.add(test_client_user)
        database.session.commit()

        # Create a test client
        test_client = Client(
            user_id=test_client_user.id,
            name="Test Client",
            email="client@example.com",
            password="clientpassword",
            location="Somewhere",
            phone_number="+9876543210",
            created_at=datetime.now(timezone.utc)
        )
        database.session.add(test_client)
        database.session.commit()

        # Create a test user for artisan
        test_artisan_user = User(
            username="testartisanuser",
            email="testartisan@example.com",
            password="securepassword",
            location="Somewhere",
            phone_number="+1112223333",
            role="Artisan",
            created_at=datetime.now(timezone.utc)
        )
        database.session.add(test_artisan_user)
        database.session.commit()

        # Create a test artisan
        test_artisan = Artisan(
            user_id=test_artisan_user.id,
            name="Test Artisan",
            email="artisan@example.com",
            password="artisanpassword",
            phone_number="+4445556666",
            location="Test Location",
            specialization="Engineering",
            skills="Carpentry, Plumbing",
            created_at=datetime.now(timezone.utc)
        )
        database.session.add(test_artisan)
        database.session.commit()

        # Create a test booking
        test_booking = Booking(
            client_id=test_client.id,
            artisan_id=test_artisan.id,
            status="Pending",
            request_date=datetime.now(timezone.utc),
            details=None,
            completion_date=None,
            created_at=datetime.now(timezone.utc)
        )
        database.session.add(test_booking)
        database.session.commit()

        # Query the booking from the database
        retrieved_booking = Booking.query.first()

        # Assertions
        assert retrieved_booking is not None
        assert retrieved_booking.client_id == test_client.id
        assert retrieved_booking.artisan_id == test_artisan.id
        assert retrieved_booking.status == "Pending"
        assert retrieved_booking.request_date is not None
        assert retrieved_booking.completion_date is None

        # Test the __repr__ method
        assert repr(retrieved_booking) ==\
            f"Booking('{retrieved_booking.id}', 'Pending')"
        # Test the to_dict method
        assert retrieved_booking.to_dict() == {
            'artisan_name': db.session.get(Artisan, test_artisan.id).name,
            'client_name': db.session.get(Client, test_client.id).name,
            'title': 'service',
            'details': None,
            'id': retrieved_booking.id,
            'status': 'Pending',
            'request_date': retrieved_booking.request_date,
            'completion_date': None
        }


def test_update_booking(app: Flask, database: SQLAlchemy):
    """ Test updating a booking object """
    with app.app_context():
        # Query the booking from the database
        booking = Booking.query.filter_by(status="Pending").first()
        booking.status = "Accepted"
        booking.completion_date = datetime.now(timezone.utc)
        database.session.commit()

        # Query the updated booking from the database
        updated_booking = Booking.query.filter_by(status="Accepted").first()
        assert updated_booking.status == "Accepted"
        assert updated_booking.completion_date is not None


def test_delete_booking(app: Flask, database: SQLAlchemy):
    """ Test deleting a booking object """
    with app.app_context():
        # Query the booking from the database
        booking = Booking.query.filter_by(status="Accepted").first()
        database.session.delete(booking)
        database.session.commit()

        # Query the deleted booking from the database
        deleted_booking = Booking.query.filter_by(status="Accepted").first()
        assert deleted_booking is None


def test_booking_validations(app: Flask, database: SQLAlchemy):
    with app.app_context():
        # Create a test user, client, and artisan
        test_user_client = User(
            username="validationclient",
            email="validationclient@example.com",
            password="securepassword",
            phone_number="+1234567890",
            role="Client",
            location="Client Location",
            created_at=datetime.now(timezone.utc),
            image_file="default.jpg"
        )
        test_user_artisan = User(
            username="validationartisan",
            email="validationartisan@example.com",
            password="securepassword",
            phone_number="+0987654321",
            location="Artisan Location",
            role="Artisan",
            created_at=datetime.now(timezone.utc),
            image_file="default.jpg"
        )
        database.session.add(test_user_client)
        database.session.add(test_user_artisan)
        database.session.commit()

        test_client = Client(
            user_id=test_user_client.id,
            name="Validation Client",
            email="validationclient@example.com",
            password="securepassword",
            phone_number="+1234567890",
            location="Client Location"
        )
        test_artisan = Artisan(
            user_id=test_user_artisan.id,
            name="Validation Artisan",
            email="validationartisan@example.com",
            password="securepassword",
            phone_number="+0987654321",
            location="Artisan Location",
            specialization="Engineering",
            skills="Test Skills"
        )
        database.session.add(test_client)
        database.session.add(test_artisan)
        database.session.commit()

        # Test creating a booking with a missing required field
        test_booking = Booking(
            artisan_id=test_artisan.id,
            title=None,
            status=None,
            completion_date=datetime.now(timezone.utc),
            details=None,
            created_at=datetime.now(timezone.utc),
            request_date=datetime.now(timezone.utc)
        )
        database.session.add(test_booking)
        with pytest.raises(IntegrityError):
            database.session.commit()
        database.session.rollback()
