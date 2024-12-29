#!/usr/bin/python3
"""
Contains Artisan Class
"""
from models.base import db, Base
from sqlalchemy_utils import PhoneNumber
from sqlalchemy import Enum
from wtforms import RadioField, SelectField
from datetime import datetime


class Artisan(Base):
    """ Representation of Artisan table """
    __tablename__ = 'artisans'

    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    name = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    phone_number = db.Column(db.String(14), nullable=False)
    location = db.Column(db.String(60))
    # Removed nullable=False in Specialization and skills; not in Registration Form
    specialization = db.Column(
        Enum('Engineering', 'Nursing', 'None', name='specialization'), default='None'
        )
    skills = db.Column(db.Text, default='None')

    # user = db.relationship("User", backref=db.backref("artisans", lazy=True))
    
    bookings = db.relationship(
        "Booking", backref="artisan",
        cascade="delete", lazy=True
        )

    def __repr__(self):
        return (f"Artisan('{self.name}', '{self.email}', {self.specialization}')")

    def to_dict(self):
        """return dictionary for the record"""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'name': self.name,
            'email': self.email,
            'phone_number': self.phone_number,
            'specialization': self.specialization,
            'sills': self.skills,
            #'bookings': [b.to_dict() for b in self.bookings] if self.bookings else None
        }