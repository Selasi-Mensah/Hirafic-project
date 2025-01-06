#!/usr/bin/env python3
"""
API for client
"""
import os
import uuid
from typing import Dict, Any, Tuple, List
from PIL import Image
from flask import Blueprint, request
from __init__ import db
from models.user import User
from models.client import Client
from models.artisan import Artisan
from forms.client import ClientProfileForm
from flask import (flash, request, current_app, jsonify)
from flask_login import current_user, login_required
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


def update_user_object(form: ClientProfileForm) -> None:
    """ Update the user object details """
    if form.picture.data:
        picture_file = save_picture(form.picture.data)
        current_user.image_file = picture_file
    current_user.username = form.username.data
    current_user.email = form.email.data
    current_user.phone_number = form.phone_number.data
    current_user.location = form.location.data


def update_client_object(form: ClientProfileForm) -> None:
    """ Update the client object details """
    if not current_user.client:
        current_user.client = Client(user=current_user)
    current_user.client.name = form.username.data
    current_user.client.email = form.email.data
    current_user.client.phone_number = form.phone_number.data
    current_user.client.location = form.location.data


@clients_Bp.route("/client", methods=['GET', 'POST'], strict_slashes=False)
@clients_Bp.route("/client/<username>", methods=['GET', 'POST'],
                  strict_slashes=False)
@login_required
def client_profile(username: str = "") -> Dict[str, Any]:
    """ client profile route
    GET /client
    GET /client/<username>
    POST /client
    POST /client/<username>
        - Success: JSON with client profile
        - Error:
            - 403 if user is not authenticated
            - 403 if user is not a client
            - 400 if an error occurred during update
            - 400 if form validation failed
    """
    # check if the user is authorized to view the page
    if username != current_user.username and username != "":
        return jsonify({"error": "User not authenticated"}), 403

    # check if the user is a client
    if current_user.role != 'Client':
        return jsonify({"error": "User is not a client"}), 403

    # set up client profile form
    form = ClientProfileForm()

    # handle GET request
    if request.method == "GET":
        client_data = current_user.client.to_dict()
        client_data['image_file'] = current_user.image_file
        return jsonify(client_data), 200

    # handle POST request after validating the form
    if form.validate_on_submit():
        try:
            # update the user and client profile
            update_user_object(form)
            update_client_object(form)
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
        methods=['GET', 'POST'], strict_slashes=False)
@login_required
def nearby_artisan(username="") -> List:
    """ route to search nearby artisan
    GET /client/nearby_artisan
        - Success: JSON with nearby artisans
        - Error:
            - 403 if user is not authenticated
            - 403 if user is not a client
            - 400 if an error occurred during search
    """
    # check if the user is authorized to view the page
    if username != current_user.username and username != "":
        return jsonify({"error": "User not authenticated"}), 403

    # check if the user is a client
    if current_user.role != 'Client':
        return jsonify({"error": "User is not a client"}), 403

    try:
        # make sure to geocode the client location
        current_user.client.geocode_location()
        # get the location tuple (longitude, latitude) of the client
        current_location = (current_user.client.longitude,
                            current_user.client.latitude)

        # search for nearby artisans within 5km
        artisans = search_nearby_artisans(current_location, 5000)
        # return JSON list of nearby artisans with name, longitude and latitude
        return jsonify([{
            'name': artisan.name,
            'longitude': artisan.longitude,
            'latitude': artisan.latitude
        } for artisan in artisans])
    except Exception as e:
        # return error if unable to complete search
        return jsonify({"error": "An error occurred during search"}), 400
