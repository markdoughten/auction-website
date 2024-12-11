from hashlib import sha512
from flask import jsonify
from . import constants


def get_hash(data):
    final_pass = data + "including a random salt";
    return sha512(final_pass.encode('utf-8')).hexdigest()



def gen_resp_msg(code, status=None, msg=None):
    output={}
    
    match code:
        case 200:
            output[constants.STATUS] = constants.STATUS_RESPONSE.SUCCESS.value
            output[constants.MESSAGE] = constants.SUCCESS_MSG
        
        case 400:
            output[constants.STATUS] = constants.STATUS_RESPONSE.FAILURE.value
            output[constants.MESSAGE] = constants.INVALID_REQ

        case 404:
            output[constants.STATUS] = constants.STATUS_RESPONSE.FAILURE.value
            output[constants.MESSAGE] = constants.NOT_FOUND

        case _:
            output[constants.STATUS] = constants.STATUS_RESPONSE.FAILURE.value
            output[constants.MESSAGE] = constants.FAILURE_MSG

    return jsonify(output), code
