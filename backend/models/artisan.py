#!/usr/bin/env python3
"""
Contains Artisan Class
"""
import requests
from models.base import db, Base
from sqlalchemy import Enum


class Artisan(Base):
    """ Representation of Artisan table """
    __tablename__ = 'artisans'

    user_id = db.Column(db.Integer,
                        db.ForeignKey('users.id', ondelete='CASCADE'),
                        nullable=False)
    name = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    phone_number = db.Column(db.String(14), nullable=False)
    location = db.Column(db.String(60), nullable=False)
    # Added latitude and longitude attributes to the table 'Artisans'
    latitude = db.Column(db.Float, nullable=True)
    longitude = db.Column(db.Float, nullable=True)
    # Removed nullable=False in Specialization and skills
    specialization = db.Column(
        Enum('Engineering', 'Nursing', 'None', name='specialization'),
        default='None'
        )
    skills = db.Column(db.Text, default='None')
    bookings = db.relationship(
        "Booking", backref="artisan",
        cascade="delete", lazy=True
        )

    def __repr__(self):
        """ artisan representation method """
        return (f"Artisan('{self.name}', '{self.specialization}')")

    def to_dict(self):
        """ return dictionary for the object """
        return {
            'name': self.name,
            'email': self.email,
            'phone_number': self.phone_number,
            'location': self.location,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'specialization': self.specialization,
            'skills': self.skills,
            # 'bookings': [b.to_dict() for b in self.bookings]
            # if self.bookings else None
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
            'limit': 1            # Limit results to 1
        }

        headers = {
            'User-Agent': 'Hirafic_Project/1.0'
        }
        # send request to get the location geocode
        response = requests.get(base_url, params=params, headers=headers)

        # extract the longitude and latitude
        if response.status_code == 200:
            data = response.json()
            if data:
                location_data = data[0]
                # update object longitude and latitude
                self.latitude = float(location_data['lat'])
                self.longitude = float(location_data['lon'])
                db.session.commit()
                return True
            else:
                raise ValueError(
                    f"Could not geocode location: {self.location}")

        else:
            raise ConnectionError("Failed to connect to OpenStreetMap API.")
