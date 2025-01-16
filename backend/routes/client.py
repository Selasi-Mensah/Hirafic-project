#!/usr/bin/env python3
"""
Contains API for client
"""
import os
import uuid
from typing import Dict, Any, Tuple, List
from PIL import Image
from flask import Blueprint, request
from extensions import db
from models.user import User
from models.client import Client
from models.artisan import Artisan
from forms.client import ClientProfileForm
from flask import (flash, request, current_app, jsonify)
from flask_jwt_extended import get_jwt_identity, jwt_required
# from flask_login import current_user, login_required
from geopy.distance import geodesic


# create clients blueprint
clients_Bp = Blueprint('clients', __name__)


def save_picture(form_picture: Any) -> str:
    """ function to save the updated profile picture """
    # get a random hex to avoid file name collision
    random_hex = uuid.uuid4().hex[:8]
    # get the file extension
    _, file_ext = os.path.splitext(form_picture.filename)
    # create a unique file name
    pic_fname = random_hex + file_ext
    # create the path to save the file
    picture_path = os.path.join(current_app.root_path,
                                'static/profile_pics', pic_fname)
    # resize the image
    output_size = (125, 125)
    open_image = Image.open(form_picture)
    open_image.thumbnail(output_size)
    # save the image
    open_image.save(picture_path)
    # return the file name
    return pic_fname


def update_user_object(form: ClientProfileForm, current_user: User):
    """ Update the user object details """
    if form.picture.data:
        picture_file = save_picture(form.picture.data)
        current_user.image_file = picture_file
    current_user.username = form.username.data
    current_user.email = form.email.data
    current_user.phone_number = form.phone_number.data
    current_user.location = form.location.data


def update_client_object(form: ClientProfileForm, current_user: User):
    """ Update the client object details """
    if not current_user.client:
        current_user.client = Client(user=current_user)
    current_user.client.name = form.username.data
    current_user.client.email = form.email.data
    current_user.client.phone_number = form.phone_number.data
    current_user.client.location = form.location.data


@clients_Bp.route("/client", methods=['GET', 'POST', 'OPTIONS'],
                  strict_slashes=False)
@clients_Bp.route("/client/<username>",
                  methods=['GET', 'POST', 'OPTIONS'],
                  strict_slashes=False)
@jwt_required()
def client_profile(username: str = "") -> str:
    """ client profile route
    GET /client
    GET /client/<username>
    POST /client
    POST /client/<username>
        - form fields to update:
            - username
            - email
            - phone_number
            - location
            - picture
            - submit
        - Success : JSON with client profile
        - Error:
            - 403 if user is not authenticated
            - 403 if user is not a client
            - 400 if an error occurred during update
            - 400 if form validation failed
        - JSON body:
                - name
                - email
                - phone_number
                - location
                - latitude
                - longitude
                - image_file
                - bookings
    """
    # check OPTIONS method
    if request.method == 'OPTIONS':
        return jsonify({"message": "Preflight request"}), 200

    # check if user is authenticated
    user_id = get_jwt_identity()
    current_user = User.query.filter_by(id=user_id).first()
    if current_user:
        if username != current_user.username and username != "":
            return jsonify({"error": "User not authenticated"}), 403

    # check if the user is a client
    if current_user.role != 'Client':
        return jsonify({"error": "User is not a client"}), 403

    # set up client profile form
    form = ClientProfileForm()

    # handle GET request
    if request.method == "GET":
        # return the client object
        return jsonify(current_user.client.to_dict()), 200

    # handle POST request after validating the form
    elif form.validate_on_submit():
        try:
            # update the user and client profile
            update_user_object(form, current_user)
            update_client_object(form, current_user)
            # commit the changes
            db.session.commit()
            # flash a success message
            flash('Your profile has been updated!', 'success')
            # return the updated client object
            return jsonify(current_user.client.to_dict()), 200
        except Exception as e:
            # If an error occurs, rollback the session
            db.session.rollback()
            # return error if unable to complete registration
            return jsonify({"error": "An error occurred during updating"}), 400

    else:
        # return error if form validation failed
        return jsonify({"error": "Invalid form data"}), 400


def search_nearby_artisans(
        current_location: Tuple, max_distance_km: int) -> List:
    """
    Search nearby artisans within the max distance using geospatial queries.
        param current_location: Tuple with (latitude, longitude)
        param max_distance_km: Maximum distance in km to search for artisan
    Return: List of nearby artisans
    """
    results = []
    # search for artisans within the max distance
    for artisan in Artisan.query.all():
        # make sure to geocode location before search
        artisan.geocode_location()
        # get the artisan location
        artisan_location = (artisan.latitude, artisan.longitude)
        # calculate the distance between the current location and the artisan
        distance = geodesic(current_location, artisan_location).km
        # check if the artisan is within the max distance
        if distance <= max_distance_km:
            # add the artisan to the results
            results.append(artisan)
    # return the list of nearby artisans
    return results


@clients_Bp.route(
        "/client/<username>/nearby_artisan",
        methods=['GET', 'POST', 'OPTIONS'], strict_slashes=False)
@clients_Bp.route(
        "/nearby_artisan",
        methods=['GET', 'POST', 'OPTIONS'], strict_slashes=False)
@jwt_required()
def nearby_artisan(username: str = "") -> List:
    """ route to search nearby artisan
    GET /client/nearby_artisan
        - Success: JSON with nearby artisans
        - Error:
            - 403 if user is not authenticated
            - 403 if user is not a client
            - 400 if an error occurred during search
    """
    # check OPTIONS method
    if request.method == 'OPTIONS':
        return jsonify({"message": "Preflight request"}), 200

    # check if user is authenticated
    user_id = get_jwt_identity()
    current_user = User.query.filter_by(id=user_id).first()
    if not current_user\
            or (username != current_user.username and username != ""):
        return jsonify({"error": "User not authenticated"}), 403

    # check if the user is a client
    if current_user.role != 'Client':
        return jsonify({"error": "User is not a client"}), 403

    # get the distance from the request body
    data = request.get_json()
    if data:
        if data.get('distance'):
            distance = data.get('distance')
        else:
            distance = 5000

    try:
        # make sure to geocode the client location
        current_user.client.geocode_location()
        # get the location tuple (longitude, latitude) of the client
        current_location = (current_user.client.latitude,
                            current_user.client.longitude)

        # search for nearby artisans within 5km
        artisans = search_nearby_artisans(current_location, distance)
        # return JSON list of nearby artisans with name, longitude and latitude
        return jsonify([{
            'name': artisan.name,
            'longitude': artisan.longitude,
            'latitude': artisan.latitude
        } for artisan in artisans]), 200
    except Exception as e:
        # return error if unable to complete search
        return jsonify({"error": "An error occurred during search"}), 400
