#!/usr/bin/python3
"""
Contains User Class
"""
from models.base import db, Base
from sqlalchemy_utils import PhoneNumber
from sqlalchemy import Enum
from wtforms import RadioField, SelectField
from datetime import datetime
from  extensions import login_manager
from flask_login import UserMixin
#from models.artisan import Artisan


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
    # return db.session.get(User, int(user_id))

class User(Base, UserMixin):
    """ Representation of user table """
    __tablename__ = 'users'

    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpeg')
    password = db.Column(db.String(60), nullable=False)
    phone_number = db.Column(db.String(14), nullable=False)
    role = db.Column(
        Enum('Artisan', 'Client', name='user_role'),
        nullable=False
        )
    
    client = db.relationship("Client", backref="user_client", cascade="all, delete, delete-orphan", uselist=False)
    artisan = db.relationship("Artisan", backref="user_artisan", cascade="all, delete, delete-orphan", uselist=False)


    def to_dict(self):
        """return dictionary for the record"""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'name': self.name,
            'email': self.email,
            'phone_number': self.phone_number,
            #'bookings': [b.to_dict() for b in self.bookings] if self.bookings else None
        }

    # def __init__(self, **kwargs):
    #     """ constructor for client or artisan"""
    #     super().__init__(**kwargs)
    #     if self.role == "Artisan":
    #         self.artisan = Artisan(
    #             user_id = self.id,
    #             name = self.username,
    #             email = self.email,
    #             password = self.password,
    #             phone_number = self.phone_number
    #         )
    #     elif self.role == "Client":
    #         self.client = Client(
    #             user_id = self.id,
    #             name = self.username,
    #             email = self.email,
    #             password = self.password,
    #             phone_number = self.phone_number
    #         )

    def __repr__(self):
        """ representation of user"""
        return (f"User('{self.username}', '{self.email}')")

