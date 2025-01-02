#!/usr/bin/python
"""
Contains Registration and Login Forms
"""
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField, RadioField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from models.user import User
from flask_login import current_user


class ClientProfileForm(FlaskForm):
    """ This form for Client Profile """
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

    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'jpeg', 'png'])])

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
