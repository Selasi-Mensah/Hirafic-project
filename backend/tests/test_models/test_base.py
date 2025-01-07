import pytest
from flask import Flask
from extensions import db
from models.base import Base


@pytest.fixture(scope="module")
def app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["SECRET_KEY"] = "test_secret_key"

    # Bind SQLAlchemy to the Flask app
    db.init_app(app)

    return app


@pytest.fixture(scope="module")
def database(app):
    with app.app_context():
        db.create_all()  # Create tables
        yield db  # Provide the database object to the test
        db.drop_all()  # Clean up tables after tests


def test_base_model(database):
    """Test the Base model."""
    class TestModel(Base):
        __tablename__ = 'test_model'
        name = db.Column(db.String(50), nullable=False)

    # Create the table for TestModel
    database.create_all()

    # Create an instance of TestModel
    test_instance = TestModel(name="Test Name")
    database.session.add(test_instance)
    database.session.commit()

    # Retrieve the instance from the database
    retrieved_instance = TestModel.query.first()
    assert retrieved_instance is not None
    assert retrieved_instance.id is not None
    assert retrieved_instance.created_at is not None
    assert retrieved_instance.name == "Test Name"
