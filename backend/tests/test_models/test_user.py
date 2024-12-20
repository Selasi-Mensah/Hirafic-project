import pytest
from flask import Flask
from models.base import db
from models.user import User
from models.client import Client
from models.artisan import Artisan
from models.booking import Booking
from datetime import datetime, timezone


@pytest.fixture(scope="module")
def app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # Bind SQLAlchemy to the Flask app
    db.init_app(app)
    return app


@pytest.fixture(scope="module")
def database(app):
    with app.app_context():
        db.create_all()  # Create tables
        yield db  # Provide the database object to the test
        db.drop_all()  # Clean up tables after tests


@pytest.fixture(scope="module")
def user_model():
    """Fixture to provide access to the User model."""
    return User


def test_user_creation(app, database, user_model):
    with app.app_context():
        # Create a test user
        test_user = user_model(
            username="testuser",
            email="testuser@example.com",
            password="securepassword",
            phone_number="+1234567890",
            role="Client",
            created_at=datetime.now(timezone.utc)
        )
        database.session.add(test_user)
        database.session.commit()

        # Query the user from the database
        retrieved_user = user_model.query.filter_by(username="testuser").first()

        # Assertions
        assert retrieved_user is not None
        assert retrieved_user.username == "testuser"
        assert retrieved_user.email == "testuser@example.com"
        assert retrieved_user.phone_number == "+1234567890"
        assert retrieved_user.role == "Client"
        assert retrieved_user.created_at is not None

        # Test the __repr__ method
        assert repr(retrieved_user) == "User('testuser', 'testuser@example.com')"
