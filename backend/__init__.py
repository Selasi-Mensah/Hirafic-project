from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager


# creating flask instant and db
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SECRET_KEY'] = 'e4307d4b50f2d467b26d69469749871a'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

# when importing the modules I face issue with pytest for circular import
from models.base import Base

from models.user import User
from models.client import Client
from models.artisan import Artisan
from models.booking import Booking
from routes import auth

with app.app_context():
    db.create_all()