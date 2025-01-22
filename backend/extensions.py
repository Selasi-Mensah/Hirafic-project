#!/usr/bin/env python3
""" Initialization of Flask extensions """
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
# from flask_login import LoginManager
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_redis import FlaskRedis


db = SQLAlchemy()
migrate = Migrate()
bcrypt = Bcrypt()
# login_manager = LoginManager()
# Set cores for all resouces and origins
cors = CORS(resources={r"/*": {"origins": "*"}})
jwt = JWTManager()
redis_client = FlaskRedis()
