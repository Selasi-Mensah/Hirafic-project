#!/usr/bin/python3
"""
API for artisan
"""
from __init__ import db, app, bcrypt
from models.user import User
from models.artisan import Artisan
from forms.auth import RegistrationForm, LoginForm
from flask import redirect, render_template, url_for, flash, request
from datetime import datetime
from flask_login import login_user, current_user, logout_user, login_required


@app.route("/artisan", methods=['GET', 'POST'])
@login_required
def artisan_profile(account_name):
    #return render_template('account.html', title='Account')
    return "Artisan Profile"