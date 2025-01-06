#!/usr/bin/env python3
"""
Contains Artisan's profile form
"""
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, SubmitField, TextAreaField, SelectField
from wtforms.validators import DataRequired, Length, Email, ValidationError
from models.user import User
from flask_login import current_user


class ArtisanProfileForm(FlaskForm):
    """ This form for Artisan Profile:
    fields:
        - username
        - email
        - phone_number
        - location
        - specialization
        - skills
        - picture
        - submit
    methods:
        - validate_username
        - validate_email
        - validate_on_submit
    """
    username = StringField('Username', validators=[
                                DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[
                            DataRequired(), Email()])
    phone_number = StringField('Phone Number', validators=[DataRequired()])
    location = StringField('Location', validators=[
        DataRequired(),
        Length(
            min=2, max=100,
            message="Location must not exceed 60 characters."
            )
        ])
    specialization = SelectField('Specialization',
                                 choices=[
                                     ('Engineering', 'Engineering'),
                                     ('Nursing', 'Nursing'),
                                     ('None', 'None')],
                                 default='None')
    skills = TextAreaField('Skills', validators=[
        Length(
            max=500,
            message="Skills description must not exceed 500 characters.")])

    picture = FileField(
        'Update Profile Picture',
        validators=[FileAllowed(['jpg', 'jpeg', 'png'])])

    submit = SubmitField('Update')

    def validate_username(self, username):
        """ to validate username """
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('Username is already taken!')

    def validate_email(self, email):
        """ to validate password """
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('Email is already taken!')

    def validate_on_submit(self):
        """ Override to manually disable CSRF validation """
        if not super().validate_on_submit():
            # Manually validate CSRF token
            if self.csrf_token.errors:
                return True
            return False
        return True
