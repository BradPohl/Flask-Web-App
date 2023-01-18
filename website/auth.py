# -*- coding: utf-8 -*-
"""
Created on Thu Jan  5 11:16:21 2023

@author: bpohl
"""

from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash #NEVER STORE A PASSWORD AS PLAIN TEXT
from . import db
from flask_login import login_user, login_required, logout_user, current_user

auth = Blueprint('auth', __name__)    #(name, import_name) name does not need to be the same name as variable

"""
- Check for login method then get email and password.
- Check the password hash to ensure correct login
- Ensure email and password is in database
"""
@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Logged in Successfully!', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect password', category='error')
        else:
            flash('Email does not exist', category='error')

    return render_template("login.html", user=current_user)

"""
- Logout function
"""
@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

"""
- get entries
- check database for primary key
- check requirements, if good hash the password so we don't store plain text then store
- log the user in and send message
"""
@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        first_name = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email is already in use', category='error')

        elif len(email) < 4:
            flash('Email must be greater than 4 characters', category='error')
        elif len(first_name) < 2:
            flash('First Name must be greater than 2 characters', category='error')
        elif password1 != password2:
            flash('Passwords do not match', category='error')
        elif len(password1) < 7:
            flash('Password must be greater than 7 characters', category='error')
        else:
            new_user = User(email=email, first_name=first_name, password=generate_password_hash(password1, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            login_user(user, remember=True)
            
            flash('Account created', category='success')
            return redirect(url_for('views.home'))

    return render_template("sign_up.html", user = current_user)
