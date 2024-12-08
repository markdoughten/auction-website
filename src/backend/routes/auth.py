from flask import Blueprint, render_template
from flask import request, jsonify
from flask import current_app as app
from flask_jwt_extended import (create_access_token, jwt_required, get_jwt_identity)
from ..utils import constants
from ..utils.misc import get_hash
from ..models.user import User, add_new
from .. import jwt

auth_bp = Blueprint('auth_bp', __name__)

@auth_bp.route('/login', methods=["GET", "POST"])
def login():
    if request.method == 'GET':
        # Render the login page when accessed via GET
        return render_template('login.html')

    # Process login when accessed via POST
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        output = {}

        # Validate input
        if not email or not password:
            output['status'] = 'failure'
            output['message'] = 'Email and password are required.'
            return render_template('login.html', message=output['message']), 400

        # Query the database for the user
        user = User.query.filter_by(email=email).first()

        # Verify user exists and password matches
        if user and check_password_hash(user.password, password):
            access_token = create_access_token(identity=user.id)  # Use unique user identifier
            return jsonify({
                'status': 'success',
                'message': 'Login successful.',
                'jwt_token': access_token
            }), 200

        # Invalid credentials
        return render_template('login.html', message='Invalid email or password.'), 401

@auth_bp.route('/signup', methods=["GET", "POST"])
def signup():
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

        # Add logic to create a new user in the database here
        # For example: User.create(email=email, username=username, password=hash_password(password))

        return render_template('signup.html', message="Account created successfully!")

@auth_bp.route('/c_account', methods=["POST"])
@jwt_required()
def create_account():
    identity = get_jwt_identity()
    print(identity)
    output = {}
    if request.method == 'POST' and request.json and add_new_wrapper(request, constants.USER_ROLE.STAFF):
        output[constants.STATUS] = constants.STATUS_RESPONSE.SUCCESS.value
        output[constants.MESSAGE] = constants.SUCCESS_MSG
        return jsonify(output)

    output[constants.STATUS] = constants.STATUS_RESPONSE.FAILURE.value
    output[constants.MESSAGE] = constants.FAILURE_MSG
    return jsonify(output)