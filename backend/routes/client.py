#!/usr/bin/env python3
"""
Contains API for client
"""
import os
import uuid
from typing import Dict, Any, Tuple, List
from PIL import Image
from flask import Blueprint, request
from werkzeug.datastructures import MultiDict
from extensions import db
from models.user import User
from models.client import Client
from models.artisan import Artisan
from models.booking import Booking
from models.report import Report
from forms.client import ClientProfileForm
from flask import (flash, request, current_app, jsonify)
from flask_jwt_extended import get_jwt_identity, jwt_required
# from flask_login import current_user, login_required
from geopy.distance import geodesic
from utils.email_service import send_email


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
    #  Select path depending on the os
    if os.name == 'nt':
        # Windows path
        file_path = 'static\\profile_pics'
    else:
        # Unix/Linux/Mac path
        file_path = 'static/profile_pics'
    # create the path to save the file
    picture_path = os.path.join(current_app.root_path, file_path, pic_fname)
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
        if current_user.image_file != form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
    current_user.username = form.username.data
    current_user.email = form.email.data.lower()
    current_user.phone_number = form.phone_number.data
    current_user.location = form.location.data


def update_client_object(form: ClientProfileForm, current_user: User):
    """ Update the client object details """
    if not current_user.client:
        current_user.client = Client(user=current_user)
    current_user.client.name = form.username.data
    current_user.client.email = form.email.data.lower()
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
        - form fields to submit (POST):
            - username
            - email
            - phone_number
            - location
            - picture
            - submit
        - Success (GET, POST): return JSON with client profile
            - JSON body:
                    - name
                    - email
                    - phone_number
                    - location
                    - latitude
                    - longitude
                    - image_file
                    - bookings
        - Error (GET, POST):
            - 403 if user is not authenticated
            - 403 if user is not a client
            - 400 if an error occurred during update
            - 400 if form validation failed
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

    # Set up client profile form and disable CSRF
    form = ClientProfileForm(meta={'csrf': False})
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
        return jsonify({
            "message": "Invalid form data",
            "error": form.errors
        }), 400


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
        "/client/<username>/nearby_artisans",
        methods=['GET', 'POST', 'OPTIONS'], strict_slashes=False)
@clients_Bp.route(
        "/nearby_artisans",
        methods=['GET', 'POST', 'OPTIONS'], strict_slashes=False)
@jwt_required()
def nearby_artisan(username: str = "") -> List:
    """ route to search nearby artisan
    GET /client/<username>/nearby_artisan
    GET /nearby_artisan
        - Success: return JSON with nearby artisans
            - JSON body:
                - name
                - email
                - phone_number
                - image_file
                - skills
                - specialization
                - location
                - longitude
                - latitude
        - Error:
            - 403 if user is not authenticated
            - 401 if user is not a client (forbiden)
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

    # check if the user is nor a client
    if current_user.role != 'Client':
        return jsonify({"error": "User is not a client"}), 401

    # get the distance from the request body in km
    if request.method == 'POST':
        try:
            data = request.get_json(silent=True)
            distance = data.get('distance', 5) if data else 5
            distance = int(distance)
            if distance < 0:
                return jsonify({"error": "Invalid distance"}), 400
        except Exception as e:
            # return error if unable to get distance
            return jsonify({"error": "An error occurred during search"}), 400
    else:
        distance = 5

    try:
        # distance must be in km from the request 1km = 1000m
        # defautl distance is 5km
        # make sure to geocode the client location
        current_user.client.geocode_location()
        # get the location tuple (longitude, latitude) of the client
        current_location = (current_user.client.latitude,
                            current_user.client.longitude)
        # search for nearby artisans within distance
        artisans = search_nearby_artisans(current_location, distance)

        # check if the request is a GET request
        arg = request.args.get('page')
        if 'page' not in request.args:
            data = [artisan.to_dict() for artisan in artisans]
            sorted_artisans = sorted(data, key=lambda x: x['username'])
            return jsonify(sorted_artisans), 200
        else:
            # Get query parameters for pagination
            page = int(request.args.get('page', 1))
            per_page = int(request.args.get('per_page', 10))
            # Calculate start and end indices
            start = (page - 1) * per_page
            end = start + per_page
            # Paginate the data
            data = [artisan.to_dict() for artisan in artisans]
            sorted_artisans = sorted(data, key=lambda x: x['username'])
            paginated_data = sorted_artisans[start:end]
            total_pages = (len(data) + per_page - 1) // per_page
            # return the list of artisans and pagination info
            return jsonify({
                'artisans': paginated_data,
                'total_pages': total_pages,
                'current_page': page
            }), 200
    except Exception as e:
        # return error if unable to complete search
        return jsonify({"error": "An error occurred during search"}), 400


@clients_Bp.route(
        "/report",
        methods=['POST', 'OPTIONS'], strict_slashes=False)
@jwt_required()
def report():
    """ route to report an artisan
    GET /report
        - Success: return JSON with message
            - JSON body:
                - message
        - Error:
            - 403 if user is not authenticated
            - 401 if user is not a client (forbiden)
    """
    # check OPTIONS method
    if request.method == 'OPTIONS':
        return jsonify({"message": "Preflight request"}), 200

    # check if user is authenticated
    user_id = get_jwt_identity()
    current_user = User.query.filter_by(id=user_id).first()
    if not current_user:
        return jsonify({"error": "User not authenticated"}), 403

    # check if the user is nor a client
    if current_user.role != 'Client':
        return jsonify({"error": "User is not a client"}), 401
    try:
        data = request.get_json()
        client_name = data.get('client_name')
        artisan_name = data.get('artisan_name')
        issue = data.get('issue', '')
        booking_id = data.get('booking_id', '')

        # Validating client and artisan existence
        client = Client.query.filter_by(name=client_name).first()
        artisan = Artisan.query.filter_by(name=artisan_name).first()
        # Check if client and artisan exist
        if not client or not artisan:
            return jsonify({"error": "Client or Artisan not found"}), 404
        # Check if the booking exists
        booking = Booking.query.filter_by(id=booking_id).first()
        if not booking:
            return jsonify({"error": "Booking not found"}), 404
        # Create a report
        report = Report(
            client_id=client.id,
            artisan_id=artisan.id,
            booking_id=booking.id,
            issue=issue
        )
        db.session.add(report)
        db.session.commit()
    except Exception as e:
        return jsonify({"error": f"Invalid request: {str(e)}"}), 400

    # get the report details from the request body (sent by params)
    # try:
    #     artisan_name = request.args.get('artisan_name', "")
    #     booking_id = request.args.get('booking_id', "")
    #     issue = request.args.get('issue', "")
    #     client_name = request.args.get('client_name', "")
    # except Exception as e:
    #     # return error if unable to get report data
    #     return jsonify({"error": "An error occurred during report"}), 400

    # Sending notification email to the artisan
    subject = f"Report: An issue with {artisan_name} artisan"
    body = f"""
    Hello Hirafic Team,

    I am reporting an issue with the artisan {artisan_name},
    Booking ID: {booking_id}.
    The issue is as follows: {issue}
    please take necessary action.

    Best regards,
    {client_name}
    """
    send_email("DuaaRabie11@gmail.com", subject, body)

    return jsonify({"message": "Report sent successfully!"}), 201
