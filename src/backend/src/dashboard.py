from backend.constants import constants
from backend.src.module.auction import Auctions
from flask import request, jsonify
from backend import app
from flask_jwt_extended import jwt_required

@app.route('/get_items', methods=["POST"])
@jwt_required()
def get_items():
    output = {}
    if request.method == 'POST':
        Auctions.query.filter()
        return jsonify(output)

    output[constants.STATUS] = constants.STATUS_RESPONSE.FAILURE.value
    output[constants.MESSAGE] = constants.FAILURE_MSG
    return jsonify(output)
