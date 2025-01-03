#!/usr/bin/python3
"""creating the Flask app"""
from flask import Flask
from extensions import db, migrate, bcrypt, login_manager
from config import Config


def create_app(config_class=Config):
    # creating flask instant and db
    app = Flask(__name__)
    app.config.from_object(Config)
    # app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
    # app.config['SECRET_KEY'] = 'e4307d4b50f2d467b26d69469749871a'

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
        from routes.auth import users_Bp
        from routes.artisan import artisans_Bp
        from routes.client import clients_Bp
        from routes.handlers import errors_Bp

        app.register_blueprint(users_Bp)
        app.register_blueprint(artisans_Bp)
        app.register_blueprint(clients_Bp)
        app.register_blueprint(errors_Bp)

        db.create_all()
        
    return app

