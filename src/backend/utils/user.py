from flask_jwt_extended.utils import get_jwt_identity
from backend.utils import constants
from flask import request

def is_opr_allowed(roles):
    identity = get_jwt_identity()
    if not identity or identity.get('role') not in roles:
        return False

    if request.method == 'POST' and request.json:
        reqJson = request.json
        if identity.get('role') == constants.USER_ROLE.ADMIN.value and reqJson.get('role') == constants.USER_ROLE.ADMIN.value and identity.get('id') != reqJson["id"]:
            return False
        elif identity.get('role') == constants.USER_ROLE.STAFF.value and (reqJson.get('role') == constants.USER_ROLE.ADMIN.value or (reqJson.get('id') == constants.USER_ROLE.STAFF.value or identity.get('id') != reqJson["id"])):
            return False
        elif identity.get('id') != reqJson["id"]:
            return False

    return True
