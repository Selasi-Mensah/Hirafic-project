#!/usr/bin/python3
"""
Test artisan table creation
"""
import pytest
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from models.base import db, Base
from models.user import User
from models.artisan import Artisan
from models.client import Client
from models.booking import Booking
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
def artisan_model():
    """Fixture to provide access to the Artisan model."""
    return Artisan


def test_artisan_creation(app, database, user_model, artisan_model):
    with app.app_context():
        # Create a test user to associate with the artisan
        test_user = user_model(
            username="testuser",
            email="testuser@example.com",
            password="securepassword",
            phone_number="+1234567890",
            role="Artisan",
            created_at=datetime.now(timezone.utc)
        )
        db.session.add(test_user)
        db.session.commit()

        # Create a test artisan
        test_artisan = artisan_model(
            user_id=test_user.id,
            name="Test Artisan",
            email="artisan@example.com",
            password="artisanpassword",
            phone_number="+9876543210",
            location="Test Location",
            Specialization="Engineering",
            skills="Carpentry, Plumbing",
            created_at=datetime.now(timezone.utc)
        )
        db.session.add(test_artisan)
        db.session.commit()

        # Query the artisan from the database
        retrieved_artisan = artisan_model.query.filter_by(name="Test Artisan").first()

        # Assertions
        assert retrieved_artisan is not None
        assert retrieved_artisan.user_id == test_user.id
        assert retrieved_artisan.name == "Test Artisan"
        assert retrieved_artisan.email == "artisan@example.com"
        assert retrieved_artisan.phone_number == "+9876543210"
        assert retrieved_artisan.location == "Test Location"
        assert retrieved_artisan.Specialization == "Engineering"
        assert retrieved_artisan.skills == "Carpentry, Plumbing"
        assert retrieved_artisan.created_at is not None

        # Test the __repr__ method
        #assert repr(retrieved_artisan) == "Artisan('Test Artisan', 'artisan@example.com')"
