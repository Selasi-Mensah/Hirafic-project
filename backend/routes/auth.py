#!/usr/bin/env python3
"""
Contains Route module for main API and users API
"""
from flask import Blueprint, jsonify, abort, request
from extensions import db, bcrypt
from models.user import User
from models.artisan import Artisan
from models.client import Client
from forms.auth import RegistrationForm, LoginForm
from flask import flash, request
from flask_login import login_user, current_user, logout_user, current_user


# create users blueprint
users_Bp = Blueprint('users', __name__)


@users_Bp.route("/home", methods=['GET'], strict_slashes=False)
@users_Bp.route("/", methods=['GET'], strict_slashes=False)
def home() -> str:
    """
    GET /home
    GET /
    Return:
        - Success: JSON with all artisans
        - Error: 404 if no artisans found
    """
    artisans = Artisan.query.all()
    if not artisans:
        abort(404)
    # return jsonify({'artisans': [artisan.to_dict() for artisan in artisans]})
    return jsonify([artisan.to_dict() for artisan in artisans])


@users_Bp.route("/register", methods=['GET', 'POST'],
                strict_slashes=False)
def register() -> str:
    """
    GET /register
        - return JSON with fields to submit
    POST /register
    Return:
        - Success: JSON with user object, 201
            - JSON body:
                - username
                - email
                - phone_number
                - location
                - role
        - Error:
            - 400 if user already authenticated
            - 500 if unable to complete registration
            - 400 if form validation failed
    """
    # check if user is already authenticated
    if current_user.is_authenticated:
        return jsonify({"error": "User already Loged in"}), 400

    # set up  registration form
    form = RegistrationForm()

    # handle GET request
    if request.method == "GET":
        return jsonify({
            "fields_to_submit": "username, email, password, "
            "confirm_password, phone_number, location, role"
            })

    # handle POST request after validating the form
    elif form.validate_on_submit():
        try:
            # hash the password before saving to DB
            hashed_password = bcrypt.generate_password_hash(
                form.password.data).decode('utf-8')
            # create user object
            user = User(
                username=form.username.data,
                email=form.email.data,
                password=hashed_password,
                phone_number=form.phone_number.data,
                location=form.location.data,
                role=form.role.data
                )
            # add user to DB
            db.session.add(user)
            db.session.commit()

            # check the role to create the related client or artisan object
            if user.role == "Client":
                # create client object
                client = Client(
                    user_id=user.id,
                    name=user.username,
                    email=user.email,
                    location=user.location,
                    password=user.password,
                    phone_number=user.phone_number
                    )
                # add client to DB
                db.session.add(client)
                db.session.commit()

            elif user.role == "Artisan":
                # create artisan object
                artisan = Artisan(
                    user_id=user.id,
                    name=user.username,
                    email=user.email,
                    location=user.location,
                    password=user.password,
                    phone_number=user.phone_number,
                    )
                # add artisan to DB
                db.session.add(artisan)
                db.session.commit()

            # flash message
            flash('Your account has been created!', 'success')
            # return user object
            return jsonify(user.to_dict()), 201

        except Exception as e:
            db.session.rollback()
            # return error if unable to complete registration
            return jsonify({"error": "Unable to complete registration"}), 500

    else:
        # return error if form validation failed
        return jsonify({"error": form.errors}), 400


@users_Bp.route("/login", methods=['GET', 'POST'], strict_slashes=False)
def login() -> str:
    """
    GET /login
        - return JSON with fields to submit
    POST /login
        - JSON body:
            - email
            - password
            - remember
            - submit
    Return:
        - Success: JSON with artisan, client or user object
        - Error:
            - 400 if user already authenticated
            - 400 if invalid email or password
            - 400 if invalid form data
    """
    # check if user is already authenticated
    if current_user.is_authenticated:
        return jsonify({"error": "User already Loged in"}), 400

    # set up login form
    form = LoginForm()

    # handle GET request
    if request.method == "GET":
        return jsonify({"fields_to_submit":
                        "email, password, remember, submit"})
    # handle POST request after validating the form
    elif form.validate_on_submit():
        # check if user exists and password is correct
        user = User.query.filter_by(email=form.email.data).first()
        if user and\
                bcrypt.check_password_hash(user.password, form.password.data):
            # login user
            login_user(user, remember=form.remember.data)
            # flash message
            flash(f'Welcome {user.username}!', 'success')

            # check user role to redirect to the correct profile
            if user.role == 'Artisan':
                # return artisan object
                return jsonify({"artisan": user.artisan.to_dict()})
            elif user.role == 'Client':
                # return client object
                return jsonify({"client": user.client.to_dict()})
            else:
                # return user object
                return jsonify({"user": user.to_dict()})
        else:
            # flash message
            flash(
                f'Login Unsuccessful, please check email and password',
                'danger'
                )
            # return error if login failed
            return jsonify({"error": "Invalid email or password"}), 400

    else:
        # return error if form validation failed
        return jsonify({"error": "Invalid form data"}), 400


@users_Bp.route("/logout", strict_slashes=False)
def logout() -> str:
    """
    GET /logout
    Return:
        - Success: JSON with logout message
        - Error: 400 if user is not authenticated
    """
    # check if user is authenticated
    if not current_user.is_authenticated:
        return jsonify({"error": "User is not authenticated"}), 400
    # logout user
    logout_user()
    return jsonify({"message": "User logged out"})


# Ignore this route please, it's for testing only
@users_Bp.route("/test")
def test():
    # with users_Bp.users_Bp_context():
    # User.query.delete()
    # Client.query.delete()
    # Artisan.query.delete()

    # user_1 = User(
    #     username="Duaa",
    #     email="Duaa@gmail.com", password="password",
    #     phone_number="0123456789", role="Artisan",
    #     created_at=datetime.utcnow())
    # db.session.add(user_1)
    # db.session.commit()
    # output = db.session.query(User).all()

    # test cascade
    # user = User.query.first()
    # db.session.delete(user)
    # db.session.commit()

    output = User.query.all()
    print(f"users: {output}")

    output = Client.query.all()
    print(f"clients: {output}")

    output = Artisan.query.all()
    print(f"artisans: {output}")

    # client = Client.query.first()
    # print(client.longitude)

    # test
    return "Test"
