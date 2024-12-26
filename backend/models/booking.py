#!/usr/bin/python3
"""
Contains Booking Class
"""
from models.base import db, Base
from sqlalchemy_utils import PhoneNumber
from sqlalchemy import Enum
from wtforms import RadioField, SelectField
from datetime import datetime


class Booking(Base):
    """ Representation of bookings table """
    __tablename__ = 'bookings'

    client_id = db.Column(
        db.Integer, db.ForeignKey('clients.id'),
        nullable=False)
    artisan_id = db.Column(
        db.Integer, db.ForeignKey('artisans.id'),
        nullable=False)
    status = db.Column(
        Enum('Pending', 'Accepted', 'Rejected', 'Completed', name='status'),
        nullable=False)
    request_date = db.Column(
        db.DateTime(timezone=True),
        server_default=db.func.now())
    completion_date = db.Column(db.DateTime(timezone=True))

    def __repr__(self):
        return (f"Booking('{self.id}', '{self.status})")
