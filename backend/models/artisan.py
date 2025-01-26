#!/usr/bin/env python3
"""
Contains Artisan Class
"""
import requests
from models.base import db, Base
from sqlalchemy import Enum
from typing import Dict, Any


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
    # let specializations be a determined by the frontend
    specialization = db.Column(db.String(20), nullable=False, default='None')
    skills = db.Column(db.Text, default='None')
    # add salary per hour attribute
    salary_per_hour = db.Column(db.Float, nullable=False, default=0.0)
    bookings = db.relationship(
        "Booking", backref="artisan",
        cascade="delete", lazy=True
        )

    def __repr__(self) -> str:
        """ artisan representation method """
        return (
            f"Artisan('{self.name}', '{self.email}, '{self.specialization}')")

    def to_dict(self) -> Dict[str, Any]:
        """ return dictionary for the object """
        try:
            artisan_bookings = [b.to_dict() for b in self.bookings]
        except Exception as e:
            # handle empty client table and empty bookings
            artisan_bookings = []

        return {
            'id': self.id,
            'username': self.name,
            'email': self.email,
            'phone_number': self.phone_number,
            'location': self.location,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'specialization': self.specialization,
            'skills': self.skills,
            'salary_per_hour': self.salary_per_hour,
            'image_file': f'/{self.user_artisan.image_file}'
            if self.user_artisan else None,
            'bookings': artisan_bookings
        }

    def geocode_location(self) -> bool:
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
