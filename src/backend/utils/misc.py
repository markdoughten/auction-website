from hashlib import sha512
from typing import Tuple
from flask_jwt_extended import get_jwt_identity
from .constants import (STATUS, STATUS_RESPONSE, MESSAGE, INSUF_PERM)

def get_hash(data):
    final_pass = data + "including a random salt";
    return sha512(final_pass.encode('utf-8')).hexdigest()


def validate_user(role) -> Tuple[dict, bool]:
    identity = get_jwt_identity()
    output = {}
    if not identity or identity["role"] not in role:
        output[STATUS] = STATUS_RESPONSE.INSUF_PERM.value
        output[MESSAGE] = INSUF_PERM
        return (output, False)

    return (output, True)
