#!/usr/bin/python3
"""
Contains Client Class
"""
from models.base import db, Base
from sqlalchemy_utils import PhoneNumber
from sqlalchemy import Enum
from wtforms import RadioField, SelectField
from datetime import datetime


class Client(Base):
    """ Representation of Client table """
    __tablename__ = 'clients'

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    name = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    # image_file = db.Column(db.String(20),
    # nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    phone_number = db.Column(db.String(14), nullable=False)

    bookings = db.relationship(
        "Booking", backref="client",
        cascade="delete", lazy=True
        )

    def __repr__(self):
        return (f"Client('{self.name}', '{self.email})")
