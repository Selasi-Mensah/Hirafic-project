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
from geopy.distance import geodesic


class Artisan(Base):
    """ Representation of Artisan table """
    __tablename__ = 'artisans'

    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    name = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    phone_number = db.Column(db.String(14), nullable=False)
    location = db.Column(db.String(60), nullable=False)
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
    # def geocode_location(self, api_key):
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
        
    
    # def search_nearby_artisans(current_location, max_distance_km):
    #     """
    #     Search nearby clients within the max distance using geospatial queries.
    #         param current_location: Tuple with (latitude, longitude)
    #         param max_distance_km: Maximum distance in kilometers to search for clients
    #     return: List of nearby clients
    #     """
    #     results = []
        
    #     for artisan in Artisan.query.all():
    #         artisan_location = (artisan.latitude, artisan.longitude)
    #         distance = geodesic(current_location, artisan_location).km
    #         if distance <= max_distance_km:
    #             results.append(artisan)
        
    #     return results
