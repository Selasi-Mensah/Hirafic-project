#!/usr/bin/env python3
"""
Contains User Class
"""
from models.base import db, Base
from sqlalchemy import Enum
# from extensions import login_manager
# from flask_login import UserMixin
from models.artisan import Artisan
from typing import Dict, Any


# @login_manager.user_loader
# def load_user(user_id: int) -> 'User':
#     return User.query.get(int(user_id))
#     # return db.session.get(User, int(user_id))


class User(Base):
    """ Representation of user table """
    __tablename__ = 'users'

    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False,
                           default='default.jpeg')
    password = db.Column(db.String(60), nullable=False)
    phone_number = db.Column(db.String(14), nullable=False)
    role = db.Column(
        Enum('Artisan', 'Client', name='user_role'),
        nullable=False
        )
    location = db.Column(db.String(60), nullable=False)

    client = db.relationship("Client", backref="user_client",
                             cascade="all, delete, delete-orphan",
                             uselist=False)
    artisan = db.relationship("Artisan", backref="user_artisan",
                              cascade="all, delete, delete-orphan",
                              uselist=False)

    def __repr__(self) -> str:
        """ user representation method """
        return (f"User('{self.username}', '{self.email}')")

    def to_dict(self) -> Dict[str, Any]:
        """ return dictionary for the object """
        return {
            'username': self.username,
            'email': self.email,
            'phone_number': self.phone_number,
            'role': self.role,
            'location': self.location,
            'image_file': self.image_file
        }
