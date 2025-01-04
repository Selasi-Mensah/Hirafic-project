#!/usr/bin/env python3
""" Initialization of Flask extensions """
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_cors import CORS


db = SQLAlchemy()
migrate = Migrate()
bcrypt = Bcrypt()
login_manager = LoginManager()
cors = CORS(resources={r"/*": {"origins": "*"}})
