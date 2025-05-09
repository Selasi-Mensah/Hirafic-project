#!/usr/bin/env python3
"""creating the Flask app"""
from datetime import timedelta
from flask import Flask
from extensions import ( db, migrate, bcrypt,
                        cors, jwt, redis_client )
from config import Config


def create_app(config_class=Config):
    # creating flask instant and db
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)
    cors.init_app(app)
    jwt.init_app(app)
    redis_client.init_app(app)
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=24)

    # csrf.init_app(app)
    # login_manager.init_app(app)
    # login_manager.login_view = 'login'
    # login_manager.login_message_category = 'info'

    # Import models (inside app context to avoid circular imports)
    with app.app_context():
        from models.base import Base
        from models.user import User
        from models.client import Client
        from models.artisan import Artisan
        from models.booking import Booking
        from models.report import Report
        from routes.auth import users_Bp
        from routes.artisan import artisans_Bp
        from routes.client import clients_Bp
        from routes.handlers import errors_Bp
        from routes.booking import booking_bp

        # Register blueprints
        app.register_blueprint(users_Bp)
        app.register_blueprint(artisans_Bp)
        app.register_blueprint(clients_Bp)
        app.register_blueprint(errors_Bp)
        app.register_blueprint(booking_bp)

        db.create_all()

    # Check if token is in blacklist
    @jwt.token_in_blocklist_loader
    def check_if_token_in_blocklist(jwt_header, jwt_payload):
        jti = jwt_payload["jti"]
        token_in_redis = redis_client.get(jti)
        return token_in_redis is not None

    return app
