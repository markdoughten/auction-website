from backend.constants import constants
from backend.src.module.users import User, get_hash, add_new
from flask import request, jsonify
from backend import app, jwt
from flask_jwt_extended import create_access_token


@jwt.user_identity_loader
def user_identity_lookup(user):
    return {"username": user.username, "role": user.role.value}


@app.route('/signup', methods=["POST"])
def signup():
    output = {}
    if request.method == 'POST' and request.json and add_new(request.json.get('email'), request.json.get('uname'), request.json.get('password')):
        output[constants.STATUS] = constants.STATUS_RESPONSE.SUCCESS.value
        output[constants.MESSAGE] = constants.SUCCESS_MSG
        return jsonify(output)

    output[constants.STATUS] = constants.STATUS_RESPONSE.FAILURE.value
    output[constants.MESSAGE] = constants.FAILURE_MSG
    return jsonify(output)


@app.route('/login', methods=["POST"])
def login():
    output = {}
    if request.method == 'POST' and request.json:
        jsonData = request.json
        email = jsonData.get('email')
        password = jsonData.get('password')
        if email and password:
            user = User.query.filter((User.email==email) & (User.password==get_hash(password))).first()
            print(user)
            if user:
                access_token = create_access_token(identity=user)
                output[constants.STATUS] = constants.STATUS_RESPONSE.SUCCESS.value
                output[constants.MESSAGE] = constants.SUCCESS_MSG
                output[constants.JWT_TOKEN] = access_token
                return jsonify(output)

    output[constants.STATUS] = constants.STATUS_RESPONSE.FAILURE.value
    output[constants.MESSAGE] = constants.FAILURE_MSG
    return jsonify(output)
