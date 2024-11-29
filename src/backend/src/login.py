from backend.constants import constants
from backend.src.users import User, get_hash
from flask import request, jsonify
from backend import app, db, jwt
from flask_jwt_extended import create_access_token


@jwt.user_identity_loader
def user_identity_lookup(user):
    return {"username": user.username, "role": user.role.value}


@app.route('/signup', methods=["POST"])
def signup():
    output = {}
    output[constants.STATUS] = constants.STATUS_RESPONSE.FAILURE.value
    if request.method == 'POST' and request.json:
        jsonData = request.json
        email = jsonData.get('email')
        username = jsonData.get('uname')
        password = jsonData.get('password')
        user = User.query.filter((User.email==email) | (User.username==username)).first()
        if (user is None) and email and username and password:
            db.session.add(User(username, email, get_hash(password)))
            db.session.commit()
            output[constants.STATUS] = constants.STATUS_RESPONSE.SUCCESS.value
            output[constants.MESSAGE] = constants.SUCCESS_MSG
        else:
            output[constants.MESSAGE] = constants.FAILURE_MSG

    return jsonify(output)


@app.route('/login', methods=["POST"])
def login():
    output = {}
    output[constants.STATUS] = constants.STATUS_RESPONSE.FAILURE.value
    if request.method == 'POST' and request.json:
        jsonData = request.json
        email = jsonData.get('email')
        password = jsonData.get('password')
        if email and password:
            user = User.query.filter((User.email==email) & (User.password==get_hash(password))).first()
            if user:
                access_token = create_access_token(identity=user)
                output[constants.STATUS] = constants.STATUS_RESPONSE.SUCCESS.value
                output[constants.JWT_TOKEN] = access_token

    return jsonify(output)
