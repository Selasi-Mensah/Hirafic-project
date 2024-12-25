#!/usr/bin/python3
"""creating the Flask app"""
from flask import Flask
from extensions import db, migrate, bcrypt, login_manager


# creating flask instant and db
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SECRET_KEY'] = 'e4307d4b50f2d467b26d69469749871a'

# Initialize extensions
db.init_app(app)
migrate.init_app(app, db)
bcrypt.init_app(app)
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

# Import models (inside app context to avoid circular imports)
with app.app_context():
    from models.base import Base
    from models.user import User
    from models.client import Client
    from models.artisan import Artisan
    from models.booking import Booking
    from routes import auth
    from routes import artisan
    from routes import client
    
    db.create_all()

