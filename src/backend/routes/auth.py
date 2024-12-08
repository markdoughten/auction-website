from flask import Blueprint, render_template
from flask import request, jsonify
from flask import current_app as app
from flask import session, redirect, url_for, flash
from flask_jwt_extended import (create_access_token, jwt_required, get_jwt_identity)
from ..utils import constants
from ..utils.hash import get_hash, check_password_hash
from ..models.user import User, add_new
from .. import jwt
from ..models.auction import Auctions

auth_bp = Blueprint('auth_bp', __name__)

@auth_bp.route('/login', methods=["GET", "POST"])
def login():
    if request.method == 'GET':
        return render_template('login.html')

    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        # Validate input
        if not email or not password:
            return render_template('login.html', message="Email and password are required.")

        # Query the database for the user
        user = User.query.filter_by(email=email).first()

        # Verify user exists and password matches
        if user and check_password_hash(user.password, password):
            # Store username in session
            session['username'] = user.username
            session['user_id'] = user.id  # Optional: Store user ID
            flash("Login successful!", "success")
            return redirect(url_for('home_bp.home'))

        # Invalid credentials
        return render_template('login.html', message="Invalid email or password.")

@auth_bp.route('/signup', methods=["GET", "POST"])
@jwt_required(optional=True)  # Allow optional authentication
def signup():
    identity = get_jwt_identity()  # Get the identity from JWT if available

    if request.method == 'GET':
        return render_template('signup.html')

    if request.method == 'POST':
        email = request.form.get('email')
        username = request.form.get('username')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')

        if not email or not username or not password or not confirm_password:
            return render_template('signup.html', message="All fields are required.")

        if password != confirm_password:
            return render_template('signup.html', message="Passwords do not match.")

        # Determine if the request is from an authenticated staff user
        if identity:
            # Logic for staff to create an account
            if add_new_wrapper(request, constants.USER_ROLE.STAFF):
                return render_template('signup.html', message="Account created by staff successfully!")
            else:
                return render_template('signup.html', message="Failed to create account. Check your input.")

        # Logic for regular user signup
        add_new(email=email, username=username, password=get_hash(password))
        return render_template('signup.html', message="Account created successfully!")

@auth_bp.route('/logout')
def logout():
    session.clear()  # Clear all session data
    flash("You have been logged out.", "info")
    return redirect(url_for('home_bp.home'))