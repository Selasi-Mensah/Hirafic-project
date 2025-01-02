#!/usr/bin/python3
"""
API for artisan
"""
import os
import uuid
from PIL import Image
from flask import Blueprint
from __init__ import db, bcrypt
from models.user import User
from models.artisan import Artisan
from forms.artisan import ArtisanProfileForm
from flask import redirect, render_template, url_for, flash, request, current_app, jsonify
from datetime import datetime
from flask_login import login_user, current_user, logout_user, login_required


artisans_Bp = Blueprint('artisans', __name__)



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


# we can make the /artisan with different route redirect to /artisan/<username>
@artisans_Bp.route("/artisan", methods=['GET', 'POST'], strict_slashes=False)
@artisans_Bp.route("/artisan/<username>", methods=['GET', 'POST'])
@login_required
def artisan_profile(username=""):
    if username != current_user.username and username != "":
        abort(403)
    if current_user.role != 'Artisan':
        abort(403)
    form = ArtisanProfileForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        current_user.phone_number = form.phone_number.data
        current_user.location = form.location.data
        if not current_user.artisan:
            current_user.artisan = Artisan(user=current_user)
        current_user.artisan.name = form.username.data
        current_user.artisan.email = form.email.data
        current_user.artisan.phone_number = form.phone_number.data
        current_user.artisan.location = form.location.data
        current_user.artisan.specialization = form.specialization.data
        current_user.artisan.skills = form.skills.data
        db.session.commit()
        flash('Your profile has been updated!', 'success')
        return redirect(url_for('artisans.artisan_profile', username=current_user.username))
    elif request.method == "GET":
        form.username.data = current_user.username
        form.email.data = current_user.email
        form.phone_number.data = current_user.phone_number
        form.location.data = current_user.location
        form.specialization.data = current_user.artisan.specialization
        form.skills.data = current_user.artisan.skills
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    #return render_template('account.html', title='Account')
    return render_template('artisan.html', title='Artisan Profile', image_file=image_file, form=form, username=username)


@artisans_Bp.route('/location')
def location():
    # current_user.artisan.latitude = 37.7749
    # current_user.artisan.longitude =  -122.4194
    map = current_user.artisan.geocode_location()
    if map:
        return jsonify(
            {
                'lat': current_user.artisan.latitude,
                'long': current_user.artisan.longitude

            }
        )
    # geocode_location = {"latitude": 37.7749, "longitude": -122.4194}  # Example data
    # return render_template('location.html', geocode_location=map)

# @artisans_Bp.route("/artisan/map_search", methods=['GET', 'POST'], strict_slashes=False)
# @login_required
# def search_artisan():
#     current_user.artisan.geocode_location()
#     current_location = (current_user.artisan.longitude, current_user.artisan.latitude)
#     artisans = current_user.artisan.search_nearby_artisans(current_location, 500)
#     return jsonify(artisans)
    
