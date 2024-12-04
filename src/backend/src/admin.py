from backend.constants import constants
from backend.src.module.users import add_new
from flask import request, jsonify
from backend import app
from flask_jwt_extended import jwt_required


@app.route('/c_account', methods=["POST"])
@jwt_required()
def create_account():
    output = {}
    if request.method == 'POST' and request.json and add_new(request.json.get('email'), \
        request.json.get('uname'), request.json.get('password'), constants.USER_ROLE.STAFF):
        output[constants.STATUS] = constants.STATUS_RESPONSE.SUCCESS.value
        output[constants.MESSAGE] = constants.SUCCESS_MSG
        return jsonify(output)

    output[constants.STATUS] = constants.STATUS_RESPONSE.FAILURE.value
    output[constants.MESSAGE] = constants.FAILURE_MSG
    return jsonify(output)
