from flask import jsonify
from . import constants

def gen_resp_msg(code, status=None, msg=None, data=None):

    output = {}

    # Map of HTTP status codes to default responses
    default_responses = {
        200: (constants.STATUS_RESPONSE.SUCCESS.value, constants.SUCCESS_MSG),
        400: (constants.STATUS_RESPONSE.FAILURE.value, constants.INVALID_REQ),
        404: (constants.STATUS_RESPONSE.FAILURE.value, constants.NOT_FOUND),
        403: (constants.STATUS_RESPONSE.INSUF_PERM.value, constants.INSUF_PERM)
    }

    # Fallback for unhandled status codes
    default_status, default_msg = constants.STATUS_RESPONSE.FAILURE.value, constants.FAILURE_MSG

    # Get status and message for the given code
    status, message = default_responses.get(code, (default_status, default_msg))

    # Allow overrides if provided
    output[constants.STATUS] = status if not status else status
    output[constants.MESSAGE] = msg if msg else message
    if data:
        output[constants.DATA] = data

    return jsonify(output), code



def gen_success_response(data):
    return gen_resp_msg(200, constants.STATUS_RESPONSE.SUCCESS.value, constants.SUCCESS_MSG, data)
