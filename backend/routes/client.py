#!/usr/bin/python3
"""
API for client
"""
from __init__ import db, app, bcrypt
from models.user import User
from models.client import Client
from forms.auth import RegistrationForm, LoginForm
from flask import redirect, render_template, url_for, flash, request
from datetime import datetime
from flask_login import login_user, current_user, logout_user, login_required


@app.route("/client", methods=['GET', 'POST'])
@login_required
def client_profile():
    #return render_template('account.html', title='Account')
    return "Client Profile"