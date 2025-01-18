#!/usr/bin/env python3
"""
Contains Client Class
"""
import requests
from models.base import db, Base
from models.user import User


class Client(Base):
    """ Representation of Client table """
    __tablename__ = 'clients'

    user_id = db.Column(db.Integer,
                        db.ForeignKey('users.id', ondelete='CASCADE'),
                        nullable=False)
    name = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    phone_number = db.Column(db.String(14), nullable=False)
    location = db.Column(db.String(60), nullable=False)
    # Added latitude and longitude attributes to the table 'Clients'
    latitude = db.Column(db.Float, nullable=True)
    longitude = db.Column(db.Float, nullable=True)
    bookings = db.relationship(
        "Booking", backref="client",
        cascade="delete", lazy=True
        )

    def __repr__(self):
        """ client representation method """
        return (f"Client('{self.name}', '{self.email}')")

    def to_dict(self):
        """ return dictionary for the object """
        if not hasattr(self.bookings, 'artisan_id') or not self.bookings:
            # handle empty artisan table and empty bookings
            client_bookings = None
        else:
            client_bookings = [b.to_dict() for b in self.bookings]

        return {
            'name': self.name,
            'email': self.email,
            'phone_number': self.phone_number,
            'location': self.location,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'image_file': self.user_client.image_file
            if self.user_client else None,
            'bookings': client_bookings
        }

    def geocode_location(self):
        """
        Fetch latitude and longitude for the location using
        OpenStreetMap's Nominatim API.
        """
        if not self.location:
            raise ValueError("Location is not set for this client.")

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
                self.latitude = float(location_data['lat'])
                self.longitude = float(location_data['lon'])
                db.session.commit()
                return True
            else:
                raise ValueError(
                    f"Could not geocode location: {self.location}")

        else:
            raise ConnectionError("Failed to connect to OpenStreetMap API.")
