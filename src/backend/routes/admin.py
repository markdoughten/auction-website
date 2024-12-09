from flask import current_app as app
from flask_jwt_extended import jwt_required
from ..utils.misc import gen_resp_msg

@app.route('/get_report', methods=["POST"])
@jwt_required()
def get_report():
    return gen_resp_msg(403)
    # output, retval = misc.validate_user(constants.ADMIN_ACCESS)
    # if not retval:
    #     return output
