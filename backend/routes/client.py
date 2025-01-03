#!/usr/bin/python3
"""
API for client
"""
import os
import uuid
from PIL import Image
from flask import Blueprint, request, abort
from __init__ import db, bcrypt
from models.user import User
from models.client import Client
from models.artisan import Artisan
from forms.client import ClientProfileForm
from flask import redirect, render_template, url_for, flash, request, current_app, jsonify
from datetime import datetime
from flask_login import login_user, current_user, logout_user, login_required
from geopy.distance import geodesic


clients_Bp = Blueprint('clients', __name__)


def save_picture(form_picture):
    """ function to save the updated profile picture"""
    random_hex = uuid.uuid4().hex[:8]
    _, file_ext = os.path.splitext(form_picture.filename)
    pic_fname = random_hex + file_ext
    picture_path = os.path.join(current_app.root_path, 'static/profile_pics', pic_fname)
    
    output_size = (125, 125)
    open_image = Image.open(form_picture)
    open_image.thumbnail(output_size)
    
    open_image.save(picture_path)
    return pic_fname


@clients_Bp.route("/client", methods=['GET', 'POST'], strict_slashes=False)
@clients_Bp.route("/client/<username>", methods=['GET', 'POST'], strict_slashes=False)
@login_required
def client_profile(username=""):
    form = ClientProfileForm()
    if username != current_user.username and username != "":
        abort(403)
    if current_user.role != 'Client':
        abort(403)
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        current_user.phone_number = form.phone_number.data
        current_user.location = form.location.data
        if not current_user.client:
            current_user.client = Client(user=current_user)
        current_user.client.name = form.username.data
        current_user.client.email = form.email.data
        current_user.client.phone_number = form.phone_number.data
        current_user.client.location = form.location.data
        db.session.commit()
        flash('Your profile has been updated!', 'success')
        return redirect(url_for('clients.client_profile', username=current_user.username))
    elif request.method == "GET":
        form.username.data = current_user.username
        form.email.data = current_user.email
        form.phone_number.data = current_user.phone_number
        form.location.data = current_user.location
    #return render_template('account.html', title='Account')
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('client.html', title='Client Profile', image_file=image_file, form=form, username=username)


def search_nearby_artisans(current_location, max_distance_km):
        """
        Search nearby clients within the max distance using geospatial queries.
            param current_location: Tuple with (latitude, longitude)
            param max_distance_km: Maximum distance in kilometers to search for clients
        return: List of nearby clients
        """
        results = []
        
        for artisan in Artisan.query.all():
            artisan_location = (artisan.latitude, artisan.longitude)
            distance = geodesic(current_location, artisan_location).km
            if distance <= max_distance_km:
                results.append(artisan)
        
        return results


@clients_Bp.route("/client/map_search", methods=['GET', 'POST'], strict_slashes=False)
@login_required
def search_artisan():
    current_user.client.geocode_location()
    current_location = (current_user.client.longitude, current_user.client.latitude)
    artisans = search_nearby_artisans(current_location, 5000)
    for artisan in artisans:
        artisan.geocode_location()
    return jsonify([{
        'name': artisan.name,
        'longitude': artisan.longitude,
        'latitude': artisan.latitude
    } for artisan in artisans])
