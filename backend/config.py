#!/usr/bin/env python3
""" Include Config Class """
from datetime import timedelta


class Config:
    """ The configuration class"""
    SQLALCHEMY_DATABASE_URI = 'sqlite:///test.db'
    SECRET_KEY = 'e4307d4b50f2d467b26d69469749871a'
    JWT_SECRET_KEY = '98f58d28793de61017a23ea99acc0afc'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # Determin Expiration time for the token
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)
    # Determine (sub) claim shouldn't be verified in the JWT
    # To pass error ("msg": "Subject must be a string")
    JWT_VERIFY_SUB = False
    REDIS_URL = "redis://localhost:6379/0"
