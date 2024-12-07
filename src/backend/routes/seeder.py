from flask import request, jsonify
from flask import current_app as app
from ..utils import constants
from ..tools.seed_item_meta import seed_item_meta



@app.route('/seed/item_meta', methods=["POST"])
def add_item_meta():
    output = {}

    seed_item_meta()

    output[constants.STATUS] = constants.STATUS_RESPONSE.SUCCESS.value
    output[constants.MESSAGE] = constants.SUCCESS_MSG
    return jsonify(output)