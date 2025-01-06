#!/usr/bin/env python3
"""
API for artisan
"""
import os
import uuid
from PIL import Image
from flask import Blueprint
from __init__ import db
from models.artisan import Artisan
from forms.artisan import ArtisanProfileForm
from flask import (flash, request, current_app, jsonify)
from flask_login import current_user, login_required


# create artisans blueprint
artisans_Bp = Blueprint('artisans', __name__)


def save_picture(form_picture):
    """ function to save the updated profile picture"""
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
    return pic_fnam


def update_user_object(form):
    """ Update the user object details """
    if form.picture.data:
        picture_file = save_picture(form.picture.data)
        current_user.image_file = picture_file
    current_user.username = form.username.data
    current_user.email = form.email.data
    current_user.phone_number = form.phone_number.data
    current_user.location = form.location.data


def update_artisan_object(form):
    """ Update the artisan object details """
    if not current_user.artisan:
        current_user.artisan = Artisan(user=current_user)
    current_user.artisan.name = form.username.data
    current_user.artisan.email = form.email.data
    current_user.artisan.phone_number = form.phone_number.data
    current_user.artisan.location = form.location.data
    current_user.artisan.specialization = form.specialization.data
    current_user.artisan.skills = form.skills.data


@artisans_Bp.route("/artisan", methods=['GET', 'POST'], strict_slashes=False)
@artisans_Bp.route(
    "/artisan/<username>", methods=['GET', 'POST'], strict_slashes=False)
@login_required
def artisan_profile(username=""):
    """ artisan profile route
    GET /artisan
    GET /artisan/<username>
    POST /artisan
    POST /artisan/<username>
    Return:
        - Success: JSON with artisan object
        - Error:
            - 403 if user is not authenticated
            - 403 if user is not an artisan
            - 400 if an error occurred during update
            - 400 if form validation failed
    """
    # check if user is authenticated
    if username != current_user.username and username != "":
        return jsonify({"error": "User not authenticated"}), 403

    # check if user is an artisan
    if current_user.role != 'Artisan':
        return jsonify({"error": "User is not an artisan"}), 403

    # set up  artisan profile form
    form = ArtisanProfileForm()

    # handle GET request
    if request.method == "GET":
        # return the artisan object
        artisan_data = current_user.artisan.to_dict()
        artisan_data['image_file'] = current_user.image_file
        return jsonify(artisan_data), 200

    # handle POST request after validating the form
    if form.validate_on_submit():
        try:
            # update the user and artisan profile
            update_user_object(form)
            update_artisan_object(form)
            # commit the changes
            db.session.commit()
            # flash a success message
            flash('Your profile has been updated!', 'success')
            # return the updated artisan object
            return jsonify(current_user.artisan.to_dict()), 200
        except Exception as e:
            # If an error occurs, rollback the session
            db.session.rollback()
            # return error if unable to complete registration
            return jsonify(
                {"error": "An error occurred during updating"}), 400

    else:
        # return error if form validation failed
        return jsonify({"error": "Invalid form data"}), 400


@artisans_Bp.route('/location')
@login_required
def location():
    """ route to get the location of the artisan
    GET /location
        Return:
        - Success: JSON with latitude and longitude
        - Error:
            - 403 if user is not authenticated
            - 403 if user is not an artisan
    """
    # check if user is authenticated
    if not current_user.is_authenticated:
        return jsonify({"error": "User not authenticated"}), 403
    # check if user is an artisan
    if current_user.role != 'Artisan':
        return jsonify({"error": "User not authenticated"}), 403
    # get the location of the artisan
    map = current_user.artisan.geocode_location()
    if map:
        # return the latitude and longitude
        return jsonify(
            {
                'lat': current_user.artisan.latitude,
                'long': current_user.artisan.longitude
            }
        )
