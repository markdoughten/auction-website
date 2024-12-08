from flask import current_app as app
from flask import (request, jsonify)
from flask_jwt_extended import jwt_required
from ..utils import (constants, misc)


@app.route('/get_report', methods=["POST"])
@jwt_required()
def get_report():
    output, retval = misc.validate_user(constants.ADMIN_ACCESS)
    if not retval:
        return output
