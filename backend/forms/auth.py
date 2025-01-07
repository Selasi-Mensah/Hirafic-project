#!/usr/bin/env python3
"""
Contains Registration and Login Forms
"""
from flask_wtf import FlaskForm
from wtforms import (StringField, PasswordField, SubmitField,
                     BooleanField, RadioField)
from wtforms.validators import (DataRequired, Length, Email,
                                EqualTo, ValidationError)
from models.user import User


class RegistrationForm(FlaskForm):
    """ This form for registration:
     fields:
        - username
        - email
        - password
        - confirm_password
        - phone_number
        - location
        - role
    methods:
        - validate_username
        - validate_email
        - validate_on_submit
    """
    username = StringField('Username', validators=[DataRequired(),
                                                   Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField(
        'Confirm Password',
        validators=[DataRequired(), EqualTo('password')])
    phone_number = StringField('Phone Number', validators=[DataRequired()])
    location = StringField('Location', validators=[
        DataRequired(),
        Length(
            min=2, max=100,
            message="Location must not exceed 60 characters."
            )]
        )
    role = RadioField(
        'Role',
        choices=[('Artisan', 'Artisan'), ('Client', 'Client')],
        validators=[DataRequired()])
    # submit = SubmitField('Sign Up')

    def validate_username(self, username: StringField) -> None:
        """ method to validate username """
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Username is already taken!')

    def validate_email(self, email: StringField) -> None:
        """ method to validate password """
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Email is already taken!')

    def validate_on_submit(self) -> bool:
        """ Override to manually disable CSRF validation """
        if not super().validate_on_submit():
            # Manually validate CSRF token
            if hasattr(self, 'csrf_token'):
                if self.csrf_token.errors:
                    return True
                return False
            return False
        return True


class LoginForm(FlaskForm):
    """ This form for Login:
    fields:
        - email
        - password
        - remember
        - submit
    """
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')
