from enum import Enum

JWT_TOKEN: str = "JWT_TOKEN"
STATUS: str = "status"
MESSAGE: str = "message"
SUCCESS_MSG: str = "Operation was a success"
FAILURE_MSG: str = "Unknown error occurred"
INVALID_REQ: str = "Invalid Request"
NOT_FOUND: str = "Not found"

class STATUS_RESPONSE(Enum):
    SUCCESS = 0
    FAILURE = 1
    MISSING_TOKEN = 2


class USER_ROLE(Enum):
    ADMIN = 'Admin'
    STAFF = 'Staff'
    USER = 'User'