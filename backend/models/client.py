#!/usr/bin/python3
"""
Contains Client Class
"""
import requests
from models.base import db, Base
from sqlalchemy_utils import PhoneNumber
from sqlalchemy import Enum
from wtforms import RadioField, SelectField
from datetime import datetime


class Client(Base):
    """ Representation of Client table """
    __tablename__ = 'clients'

    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    name = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    # # image_file = db.Column(db.String(20),
    # # nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    phone_number = db.Column(db.String(14), nullable=False)
    # user_client = db.relationship("User", backref=db.backref("client", lazy=True))
    # user_client = db.relationship('User', backref='client', passive_deletes=True)
    location = db.Column(db.String(60), nullable=False)
    # Added latitude and longitude attributes to the table 'Clients'
    latitude = db.Column(db.Float, nullable=True)
    longitude = db.Column(db.Float, nullable=True)

    bookings = db.relationship(
        "Booking", backref="client",
        cascade="delete", lazy=True
        )

    def __repr__(self):
        return (f"Client('{self.name}', '{self.email}')")
    
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
    

    def geocode_location(self):
        """
        Fetch latitude and longitude for the location using
        OpenStreetMap's Nominatim API.
        """
        if not self.location:
            raise ValueError("Location is not set for this artisan.")
        
        base_url = "https://nominatim.openstreetmap.org/search"
        params = {
            'q': self.location,  # 'q' is the query parameter for the location
            'format': 'json',     # Response format in JSON
            'limit': 1            # Limit results to 1 (you can adjust as needed)
        }
        
        headers = {
            'User-Agent': 'Hirafic_Project/1.0'  # Always include a User-Agent
        }
        
        response = requests.get(base_url, params=params, headers=headers)

        if response.status_code == 200:
            data = response.json()
            if data:
                location_data = data[0]
                self.latitude = float(location_data['lat'])
                self.longitude = float(location_data['lon'])
                db.session.commit()
                return True
            else:
                raise ValueError(f"Could not geocode location: {self.location}")
        
        else:
            raise ConnectionError("Failed to connect to OpenStreetMap API.")
