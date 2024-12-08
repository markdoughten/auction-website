from enum import Enum

JWT_TOKEN: str = "JWT_TOKEN"
STATUS: str = "status"
MESSAGE: str = "message"
SUCCESS_MSG: str = "Operation was a success"
FAILURE_MSG: str = "Unknown error occurred"
INVALID_REQ: str = "Invalid Request"
INSUF_PERM: str = "User does not have sufficient permission"
NOT_FOUND: str = "Not found"
DATA: str = "data"

class STATUS_RESPONSE(Enum):
    SUCCESS = 0
    FAILURE = 1
    MISSING_TOKEN = 2
    INSUF_PERM = 3

class USER_ROLE(Enum):
    ADMIN = 'Admin'
    STAFF = 'Staff'
    USER = 'User'

ADMIN_ACCESS: list[str] = [USER_ROLE.ADMIN.value]
STAFF_ACCESS: list[str] = ADMIN_ACCESS+[USER_ROLE.STAFF.value]
USER_ACCESS: list[str] = STAFF_ACCESS+[USER_ROLE.USER.value]
