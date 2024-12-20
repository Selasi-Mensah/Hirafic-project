#!/usr/bin/python3
"""
Contains User Class
"""
from models.base import db, Base
from sqlalchemy_utils import PhoneNumber
from sqlalchemy import Enum
from wtforms import RadioField, SelectField
from datetime import datetime
from __init__ import login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(Base, UserMixin):
    """ Representation of user table """
    __tablename__ = 'users'

    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    # image_file = db.Column(db.String(20), nullable=False,
    # default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    phone_number = db.Column(db.String(14), nullable=False)
    role = db.Column(
        Enum('Artisan', 'Client', name='user_role'),
        nullable=False
        )

    client = db.relationship("Client", backref="user", cascade="delete")
    artisan = db.relationship("Artisan", backref="user", cascade="delete")

    def __repr__(self):
        return (f"User('{self.username}', '{self.email}')")

