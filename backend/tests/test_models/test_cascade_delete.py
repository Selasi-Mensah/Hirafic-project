import pytest
from flask import Flask
from __init__ import db, Base, User, Client, Artisan, Booking
from datetime import datetime, timezone


@pytest.fixture(scope="module")
def app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config['TESTING'] = True
    db.init_app(app)
    return app


@pytest.fixture
def setup_database(app):
    with app.app_context():
        db.create_all()
        yield db
        db.session.remove()
        db.drop_all()

def test_cascade_delete(app, setup_database):
    with app.app_context():
        # Create a user and associated client
        user1 = User(username='test1', email='test1@example.com', phone_number='1234567890', password='password', role='Client', created_at=datetime.now(timezone.utc))
        user2 = User(username='test2', email='test2@example.com', phone_number='1234567890', password='password', role='Artisan', created_at=datetime.now(timezone.utc))
        db.session.add(user1)
        db.session.add(user2)
        db.session.commit()
        client = Client(user_id=user1.id, name='test1', email='test1@example.com', phone_number='1234567890', password='password', created_at=datetime.now(timezone.utc))
        artisan = Artisan(user_id=user2.id, name='test2', email='test2@example.com', phone_number='1234567890', password='password', created_at=datetime.now(timezone.utc))
        # client = Client(user_client=user)
        db.session.add(client)
        db.session.add(artisan)
        db.session.commit()

        # Verify data is added
        assert User.query.count() == 2
        assert Client.query.count() == 1
        assert Artisan.query.count() == 1

        # Delete the user
        db.session.delete(user1)
        db.session.delete(user2)
        db.session.commit()

        # Verify cascade delete worked
        assert User.query.count() == 0
        assert Client.query.count() == 0
        assert Artisan.query.count() == 0
