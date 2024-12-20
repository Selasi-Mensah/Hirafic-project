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

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    name = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    # image_file = db.Column(db.String(20),
    # nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    phone_number = db.Column(db.String(14), nullable=False)
    location = db.Column(db.String(60))
    Specialization = db.Column(
        Enum('Engineering', 'Nursing', name='specialization'),
        nullable=False
        )
    skills = db.Column(db.Text, nullable=False)
    created_at = db.Column(
        db.DateTime(timezone=True),
        server_default=db.func.now()
        )
    # created_at = db.Column(db.DateTime,
    # nullable=False, default=datetime.utcnow)

    bookings = db.relationship(
        "Booking", backref="artisan",
        cascade="delete", lazy=True
        )

    def __repr__(self):
        return (f"Artisan('{self.name}', '{self.email})")
