#!/usr/bin/python3
"""
Route module for main API and users API
"""
from flask import Blueprint, jsonify, abort, request
from __init__ import db, bcrypt
from models.user import User
from models.artisan import Artisan
from models.client import Client
from forms.auth import RegistrationForm, LoginForm
from datetime import datetime
from flask import redirect, render_template, url_for, flash, request
from flask_login import login_user, current_user, logout_user, login_required, current_user


users_Bp = Blueprint('users', __name__)
# users_Bp.template_folder = 'path/to/your/templates'


@users_Bp.route("/home", methods=['GET'], strict_slashes=False)
@users_Bp.route("/", methods=['GET'], strict_slashes=False)
def home():
    """ POST /home
        POST /
    Returns:
        - list of all artisans
    """
    # artisans = Artisan.query.all()
    # if not artisans:
    #     abort(404)
    # return jsonify({'artisans': [artisan.to_dict() for artisan in artisans]})
    #return jsonify([artisan.to_dict() for artisan in artisans])
    return "Home"

@users_Bp.route("/register", methods=['GET', 'POST'], strict_slashes=False)
def registr():
    """ POST /register
        GET /register
    """
    if current_user.is_authenticated:
        return redirect(url_for('users.home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password =\
            bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(
            username=form.username.data,
            email=form.email.data,
            password=hashed_password,
            phone_number=form.phone_number.data,
            location=form.location.data,
            role=form.role.data,
            )
        #print(user)
        db.session.add(user)
        try:
            db.session.commit()
            flash('Your account has been created!', 'success')
            if user.role == "Client":
                client = Client(
                    user_id=user.id,
                    name=user.username,
                    email=user.email,
                    location=user.location,
                    password=user.password,
                    phone_number=user.phone_number
                    )
                #client_user = Client(user_client=user)
                db.session.add(client)
                db.session.commit()
            elif user.role == "Artisan":
                artisan=Artisan(
                    user_id=user.id,
                    name=user.username,
                    email=user.email,
                    location=user.location,
                    password=user.password,
                    phone_number=user.phone_number,
                    )
                db.session.add(artisan)
                db.session.commit()
            return redirect(url_for('users.login'))
            # return "register"
        except Exception as e:
            db.session.rollback()
            print(f"An error occurred during registration: {str(e)}")
            return jsonify({'error':"Registration failed"}) 400
    return render_template('register.html', titel='Register', form=form)
    #return jsonify({'user': user.to_dic()})

# @users_Bp.route('/artisan/login', methods=['GET', 'POST'])
# def artisan_login():


# @users_Bp.route('/client/login', methods=['GET', 'POST'])
# def client_login():


@users_Bp.route("/login", methods=['GET', 'POST'], strict_slashes=False)
def login():
    """ POST /login
        GET /login
    """
    if current_user.is_authenticated:
        return redirect(url_for('users.home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            if user.role == 'Artisan':
                return redirect(url_for('artisans.artisan_profile', username=user.username))
            elif user.role == 'Client':
                return redirect(url_for('clients.client_profile', username=user.username))
            else:
                next_page = request.args.get('next')
                return redirect(next_page) if next_page else redirect(url_for('users.home'))
        else:
            flash(
                f'Login Unsuccessful, please check email and password',
                'danger')
    return render_template('login.html', titel='login', form=form)
    # return "Login"


@users_Bp.route("/logout", strict_slashes=False)
def logout():
    logout_user()
    return redirect(url_for('users.home'))


# @artisan_required
# def account():
#     return render_template('account.html', title='Artisan Account')


# @client_required
# def account():
#     return render_template('account.html', title='Client Account')


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
