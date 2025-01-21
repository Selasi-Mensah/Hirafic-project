#!/usr/bin/env python3
"""
Contains Booking Class
"""
from multiprocessing.connection import Client
from models.artisan import Artisan
from models.client import Client
from models.base import db, Base
from sqlalchemy import Enum
from typing import Dict, Any


class Booking(Base):
    """ Representation of bookings table """
    __tablename__ = 'bookings'

    client_id = db.Column(
        db.Integer, db.ForeignKey('clients.id'),
        nullable=False)
    artisan_id = db.Column(
        db.Integer, db.ForeignKey('artisans.id'),
        nullable=False)
    title = db.Column(db.String(50), nullable=False, default='service')
    status = db.Column(
        Enum('Pending', 'Accepted', 'Rejected', 'Completed', name='status'),
        nullable=False, default='Pending')
    request_date = db.Column(
        db.DateTime(timezone=True),
        server_default=db.func.now())
    completion_date = db.Column(db.DateTime(timezone=True))
    details = db.Column(db.String(255), nullable=True)

    def __repr__(self) -> str:
        return (f"Booking('{self.id}', '{self.status}')")

    def to_dict(self) -> Dict[str, Any]:
        return {
            'id': self.id,
            'artisan_name': db.session.get(Artisan, self.artisan_id).name,
            'client_name': db.session.get(Client, self.client_id).name,
            'title': self.title,
            'details': self.details,
            'status': self.status,
            'request_date': self.request_date,
            'completion_date': self.completion_date
        }
