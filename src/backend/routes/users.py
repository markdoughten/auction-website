from flask import request, jsonify
from flask import current_app as app
from flask_jwt_extended import (create_access_token, jwt_required, get_jwt_identity)
from ..utils import constants
from ..utils.misc import get_hash
from ..models.user import User
from ..db_ops.user import add_new
from .. import jwt


@jwt.user_identity_loader
def user_identity_lookup(user):
    return {"username": user.username, "role": user.role.value}


def add_new_wrapper(request, user_level=constants.USER_ROLE.USER):
    return add_new(request.json.get('email'), request.json.get('uname'), request.json.get('password'), user_level)

@app.route('/signup', methods=["POST"])
def signup():
    output = {}
    if request.method == 'POST' and request.json and add_new_wrapper(request):
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


@app.route('/c_account', methods=["POST"])
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
