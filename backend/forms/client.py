#!/usr/bin/env python3
"""
Contains Client Profile form
"""
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length, Email, ValidationError
from models.user import User
from flask_jwt_extended import get_jwt_identity


class ClientProfileForm(FlaskForm):
    """ This form for Client Profile:
    fields:
        - username
        - email
        - phone_number
        - location
        - picture
        - submit
    methods:
        - validate_username
        - validate_email
        - validate_on_submit"""
    username = StringField('Username', validators=[
                                DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[
                            DataRequired(), Email()])
    phone_number = StringField('Phone Number', validators=[DataRequired()])
    location = StringField('Location', validators=[
        DataRequired(),
        Length(
            min=2, max=100,
            message="Location must not exceed 60 characters."
            )
        ])
    picture = FileField('Update Profile Picture',
                        validators=[FileAllowed(['jpg', 'jpeg', 'png'])])
    submit = SubmitField('Update')

    def validate_username(self, username: StringField) -> None:
        """ method to validate username """
        user_id = get_jwt_identity()
        current_user = User.query.filter_by(id=user_id).first()
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('Username is already taken!')

    def validate_email(self, email: StringField) -> None:
        """ method to validate password """
        user_id = get_jwt_identity()
        current_user = User.query.filter_by(id=user_id).first()
        if email.data.lower() != current_user.email:
            user = User.query.filter_by(email=email.data.lower()).first()
            if user:
                raise ValidationError('Email is already taken!')
