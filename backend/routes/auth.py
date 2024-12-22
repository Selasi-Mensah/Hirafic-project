#!/usr/bin/python3
"""
Route module for the API
"""
from __init__ import db, app, bcrypt
from models.user import User
from models.artisan import Artisan
from models.client import Client
from forms.auth import RegistrationForm, LoginForm
from flask import redirect, render_template, url_for, flash, request
from datetime import datetime
from flask_login import login_user, current_user, logout_user, login_required


@app.route("/home", methods=['GET'])
@app.route("/", methods=['GET'])
def home():
    """ POST /home
        POST /
    """
    return "Home Page"


@app.route("/register", methods=['GET', 'POST'])
def registr():
    """ POST /register
        GET /register
    """
    # if current_user.is_authenticated:
    #     return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password =\
            bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(
            username=form.username.data,
            email=form.email.data,
            password=hashed_password,
            phone_number=form.role.data,
            role=form.role.data,
            )
        #print(user)
        db.session.add(user)
        try:
            db.session.commit()
            flash('Your account has been created!', 'success')
            if user.role == "Client":
                client_user = Client(
                   user_id = user.id,
                   name = user.username,
                   email = user.email,
                   password = user.password,
                   phone_number = user.phone_number
                )
                db.session.add(client_user)
                db.session.commit()
            elif user.role == "Artisan":
                artisan_user = Artisan(
                    user_id = user.id,
                    name = user.username,
                   email = user.email,
                   password = user.password,
                   phone_number = user.phone_number,
                )
                db.session.add(artisan_user)
                db.session.commit()
            return redirect(url_for('login'))
            # return "register"
        except Exception as e:
            db.session.rollback()
            print(f"An error occurred during registration: {str(e)}")
            return "Registration failed", 400
    return render_template('register.html', titel='Register', form=form)
    #return "Registration"

# @app.route('/artisan/login', methods=['GET', 'POST'])
# def artisan_login():


# @app.route('/client/login', methods=['GET', 'POST'])
# def client_login():


@app.route("/login", methods=['GET', 'POST'])
def login():
    """ POST /login
        GET /login
    """
    # if current_user.is_authenticated:
    #     return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            # if user.role == 'Artisan':
            #     return redirect(url_for('admin_dashboard'))
            # elif user.role == 'Client':
            #     return redirect(url_for('client_dashboard'))
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash(
                f'Login Unsuccessful, please check email and password',
                'danger')
    return render_template('login.html', titel='login', form=form)
    # return "Login"


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route("/account")
@login_required
def account():
    #return render_template('account.html', title='Account')
    return "Account"

# @artisan_required
# def account():
#     return render_template('account.html', title='Artisan Account')


# @client_required
# def account():
#     return render_template('account.html', title='Client Account')


@app.route("/test")
def test():
    # test user table
    #with app.app_context():
    # User.query.delete()
    # db.session.query(User).delete()
    # db.session.commit()
    # user_1 = User(
    #     username="Duaa",
    #     email="Duaa@gmail.com", password="password",
    #     phone_number="0123456789", role="Artisan",
    #     created_at=datetime.utcnow())
    # db.session.add(user_1)
    # db.session.commit()
    # output = db.session.query(User).all()
    output = User.query.all()
    print(f"users: {output}")

    output = Client.query.all()
    print(f"clients: {output}")

    output = Artisan.query.all()
    print(f"artisans: {output}")


    # test
    return "Test"
