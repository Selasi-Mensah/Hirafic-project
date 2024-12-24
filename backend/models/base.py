#!/usr/bin/python3
"""
Contains class Base
"""
from extensions import db
from datetime import datetime, timezone


class Base(db.Model):
    """ The Abstract Base class,
    from which future classes will be derived"""
    __abstract__ = True

    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(
        db.DateTime(timezone=True),
        server_default=db.func.now(), nullable=False)
    # created_at = db.Column(db.DateTime(timezone=True),
    # nullable=False, default=datetime.utcnow)

    # def new(self, obj):
    #     """ add new object to database"""
    #     db.session.add(obj)

    # def save(self):
    #     """ save object to database """
    #     db.session.commit

    # def delete(self, obj=None):
    #     if obj is not None:
    #         db.session.delete(obj)
    
    # def all(self, cls=None):
    #     """ query on the current database session """
    #     if cls:
    #         return db.session.query(cls).all()

    #also find, update