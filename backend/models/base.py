#!/usr/bin/env python3
"""
Contains class Base
"""
from extensions import db


class Base(db.Model):
    """ The Abstract Base class,
    from which future classes will be derived"""
    __abstract__ = True

    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(
        db.DateTime(timezone=True),
        server_default=db.func.now(), nullable=False)
