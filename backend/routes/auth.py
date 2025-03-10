#!/usr/bin/env python3
"""
Contains Route module for main API and users API
"""
from flask import Blueprint, jsonify, abort, request
from extensions import db, bcrypt, redis_client
from models.user import User
from models.artisan import Artisan
from models.client import Client
from models.booking import Booking
from forms.auth import RegistrationForm, LoginForm
from flask import flash, request
# from flask_login import login_user, current_user, logout_user, current_user
from flask_jwt_extended import (create_access_token, jwt_required,
                                get_jwt_identity, get_jwt,
                                verify_jwt_in_request)
from config import Config
from werkzeug.datastructures import MultiDict


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
    if 'Authorization' in request.headers:
        try:
            verify_jwt_in_request()
            return jsonify({"error": "User already Loged in"}), 400
        except Exception as e:
            pass

    # set up registration form and disable CSRF
    form = RegistrationForm(meta={'csrf': False})

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
                email=form.email.data.lower(),
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
                    phone_number=user.phone_number,
                    )
                # geocode location
                client.geocode_location()
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
                # geocode location
                artisan.geocode_location()
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
        return jsonify({
            "message": "Invalid form data",
            "error": form.errors
        }), 400


@users_Bp.route("/login", methods=['GET', 'POST', 'OPTIONS'],
                strict_slashes=False)
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
    # check OPTIONS method
    if request.method == 'OPTIONS':
        return jsonify({"message": "Preflight request"}), 200

    # Double check if user is already authenticated
    # will be check by frontend too
    if 'Authorization' in request.headers:
        try:
            verify_jwt_in_request()
            return jsonify({"error": "User already Loged in"}), 400
        except Exception as e:
            pass

    # Convert the JSON request data to MultiDict format
    # form_data = MultiDict(request.json)
    # set up login form
    # form = LoginForm(form_data, meta={'csrf': False})
    # set up login form and disable CSRF
    form = LoginForm(meta={'csrf': False})

    # handle GET request
    if request.method == "GET":
        return jsonify({"fields_to_submit":
                        "email, password, remember, submit"})

    # handle POST request after validating the form
    elif form.validate_on_submit():
        # check if user exists and password is correct
        user = User.query.filter_by(email=form.email.data.lower()).first()
        if user and\
                bcrypt.check_password_hash(user.password, form.password.data):
            # login user
            # login_user(user, remember=form.remember.data)
            access_token = create_access_token(identity=user.id)

            # flash message
            flash(f'Welcome {user.username}!', 'success')

            return jsonify({
                "message": "Login successful",
                "access_token": access_token,
                "user": user.to_dict()
                }), 200
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
        return jsonify({
            "message": "Invalid form data",
            "error": form.errors
        }), 400


@users_Bp.route("/logout", methods=['GET', 'OPTIONS'],
                strict_slashes=False)
@jwt_required()
def logout() -> str:
    """
    GET /logout
    Return:
        - Success: JSON with logout message
        - Error: 400 if user is not authenticated
    """
    # handle OPTIONS method
    if request.method == 'OPTIONS':
        return jsonify({"message": "Preflight request"}), 200
    # check if user is authenticated
    try:
        verify_jwt_in_request()
    except Exception as e:
        return jsonify({"error": "User is not authenticated"}), 400
    # logout user
    jti = get_jwt()["jti"]
    redis_client.set(jti, "", ex=Config.JWT_ACCESS_TOKEN_EXPIRES)
    return jsonify({"message": "User logged out"}), 200


@users_Bp.route("/delete_account", methods=['DELETE', 'OPTIONS'],
                strict_slashes=False)
@jwt_required()
def delete_account() -> str:
    """
    GET /delete_account
    POST /delete_account
    Return:
        - Success: JSON with message
        - Error: 401 if user is not authenticated
    """
    # check OPTIONS method
    if request.method == 'OPTIONS':
        return jsonify({"message": "Preflight request"}), 200

    # Double check if user is authenticated
    user_id = get_jwt_identity()
    user = User.query.filter_by(id=user_id).first()
    if not user:
        return jsonify({"error": "User not authenticated"}), 401

    # check if user has bookings
    bookings = Booking.query.filter_by(user_id=user.id).all()

    if bookings:
        for booking in bookings:
            # check all user's bookings
            if booking.status != "Completed":
                # return error if user has bookings not completed
                return jsonify(
                    {"error": "Cannot delete account with existing bookings"}
                ), 400

    # delete user account
    # later we can add a confirmation step
    try:
        db.session.delete(user)
        db.session.commit()
        # logout user
        jti = get_jwt()["jti"]
        redis_client.set(jti, "", ex=Config.JWT_ACCESS_TOKEN_EXPIRES)
        # frontend should handle the redirection and token deletion
        return jsonify({"message": "Account deleted"}), 200
    except Exception as e:
        return jsonify({"error": "Unable to delete account"}), 500


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

    artisan = Artisan.query.filter_by(location="Shimokizukuri").first()
    if artisan:
        artisan.location = "Japan"
        print(artisan)

    db.session.commit()

    # delete all users
    # Must use ORM deletion to trigger cascade delete
    # User.query.delete() won't trigger cascade delete
    # users = User.query.all()
    # for user in users:
    #     db.session.delete(user)

    # db.session.commit()

    # delete all clients without cascade delete
    # Artisan.query.delete()
    # Client.query.delete()
    # User.query.delete()
    # Booking.query.delete()
    # db.session.commit()

    # test
    return "Test"
