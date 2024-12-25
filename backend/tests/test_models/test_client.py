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
def User_model():
    """Fixture to provide access to User model."""
    return User


@pytest.fixture(scope="module")
def Client_model():
    """Fixture to provide access to Client model."""
    return Client


def test_client_creation(app, database, User_model, Client_model):
    with app.app_context():
        #Create a test user to associate with the client
        test_user = User_model(
            username="testclientuser",
            email="testclientuser@example.com",
            password="securepassword",
            phone_number="+1234567890",
            role="Client",
            created_at=datetime.now(timezone.utc)
        )
        database.session.add(test_user)
        database.session.commit()

        # Create a test client
        # Client_model = client_model["Client"]
        test_client = Client_model(
            user_id=test_user.id,
            name="Test Client",
            email="client@example.com",
            password="clientpassword",
            phone_number="+9876543210",
            created_at=datetime.now(timezone.utc)
        )
        database.session.add(test_client)
        database.session.commit()

        # Query the client from the database
        retrieved_client = Client_model.query.filter_by(name="Test Client").first()

        # Assertions
        assert retrieved_client is not None
        assert retrieved_client.user_id == test_user.id
        assert retrieved_client.name == "Test Client"
        assert retrieved_client.email == "client@example.com"
        assert retrieved_client.phone_number == "+9876543210"

        # Test the __repr__ method
        assert repr(retrieved_client) == "Client('Test Client', 'client@example.com')"
        
        # Test the cascade delete
        assert User.query.count() == 1
        assert Client.query.count() == 1

        db.session.delete(test_user)

        assert User.query.count() == 0
        assert Client.query.count() == 0
