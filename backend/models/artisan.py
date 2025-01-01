#!/usr/bin/python3
"""
Contains Artisan Class
"""
import requests
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
    # Added latitude and longitude attributes to the table 'Artisans'
    latitude = db.Column(db.Float, nullable=True)
    longitude = db.Column(db.Float, nullable=True)
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

    # Added latitude and longitude to the dictionary output for easier API consumption.
    def to_dict(self):
        """return dictionary for the record"""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'name': self.name,
            'email': self.email,
            'phone_number': self.phone_number,
            'location': self.location,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'specialization': self.specialization,
            'sills': self.skills,
            #'bookings': [b.to_dict() for b in self.bookings] if self.bookings else None
        }
    
    # Geosoding method to fetch latitude and longitude for the location
    # def geocode_locatio(self, api_key):
    #     """
    #     Fetch latitude and longitude for the location using
    #     Google Geocoding API
    #     """
    #     if not self.location:
    #         raise ValueError("Location is not set for this artisan.")
        
    #     base_url = "https://maps.googleapis.com/maps/api/geocode/json"
    #     params = {
    #         'address': self.location,
    #         'key': api_key
    #     }
    #     response = requests.get(base_url, params=params)

    #     if response.status_code == 200:
    #         data = response.json()
    #         if data['results']:
    #             location_data = data['results'][0]['geometry']['location']
    #             self.latitude = location_data['lat']
    #             self.longitude = location_data['lng']
    #             return True
    #         else:
    #             raise ValueError(f"Could not geocode location: {self.location}")
            
    #     else:
    #         raise ConnectionError("Failed to connect to Google Geocoding API.")

