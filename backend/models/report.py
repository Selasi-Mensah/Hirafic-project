#!/usr/bin/env python3
"""
Contains Report Class
"""
from models.base import db, Base
from typing import Dict, Any


class Report(Base):
    """ Representation of Reports table """
    __tablename__ = 'reports'

    client_id = db.Column(
        db.Integer, db.ForeignKey('clients.id'),
        nullable=False)
    artisan_id = db.Column(
        db.Integer, db.ForeignKey('artisans.id'),
        nullable=False)
    booking_id = db.Column(
        db.Integer, db.ForeignKey('bookings.id'), nullable=False)
    issue = db.Column(db.Text, nullable=True)

    def __repr__(self) -> str:
        return (f"Report('{self.id}', '{self.issue}')")

    def to_dict(self) -> Dict[str, Any]:
        return {
            'id': self.id,
            'artisan_id': self.artisan_id,
            'client_id': self.client_id,
            'booking_id': self.booking,
            'issue': self.issue
        }
