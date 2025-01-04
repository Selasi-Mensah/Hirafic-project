#!/usr/bin/python
"""
Contains Registration and Login Forms
"""
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField, RadioField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from models.user import User
from flask_login import current_user

class RegistrationForm(FlaskForm):
    """ This form for registration """
    username = StringField('Username', validators=[
                                DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[
                            DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[
                                                        DataRequired(),
                                                        EqualTo('password')])
    phone_number = StringField('Phone Number', validators=[DataRequired()])
    location = StringField('Location', validators=[
        DataRequired(),
        Length(
            min=2, max=100,
            message="Location must not exceed 60 characters."
            )
        ])
    role = RadioField(
        'Role',
        choices=[('Artisan', 'Artisan'), ('Client', 'Client')],
        validators=[DataRequired()])
    
    # submit = SubmitField('Sign Up')

    def validate_username(self, username):
        """ to validate username """
        user = User.query.filter_by(username=username.data).first()
        if user:
            print("username issue")
            raise ValidationError('Username is already taken!')

    def validate_email(self, email):
        """ to validate password """
        user = User.query.filter_by(email=email.data).first()
        if user:
            print("email issue")
            raise ValidationError('Email is already taken!')

class LoginForm(FlaskForm):
    """ This form for Login """
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[
                                            DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

