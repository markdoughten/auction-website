from flask import request, jsonify
from flask import current_app as app
from ..utils import constants
from ..tools import seed_item_meta, seed_items



@app.route('/seed/item_meta', methods=["POST"])
def add_item_meta():
    output = {}

    seed_item_meta()

    output[constants.STATUS] = constants.STATUS_RESPONSE.SUCCESS.value
    output[constants.MESSAGE] = constants.SUCCESS_MSG
    return jsonify(output)



@app.route('/seed/items', methods=["POST"])
def add_items():
    output = {}

    seed_items()
    output[constants.STATUS] = constants.STATUS_RESPONSE.SUCCESS.value
    output[constants.MESSAGE] = constants.SUCCESS_MSG
    return jsonify(output)