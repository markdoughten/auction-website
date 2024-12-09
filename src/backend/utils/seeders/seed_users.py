import string
import random
from ...models.user import User
from .. import constants
from ..hash import get_hash
from ..common import db_create_one

def seed_users():
    usr_rng = [(100, constants.USER_ROLE.USER), (20, constants.USER_ROLE.STAFF), (1, constants.USER_ROLE.ADMIN)]
    for usr_data in usr_rng:
        for i in range(usr_data[0]):
            usr = usr_data[1].value.lower()+str(i)
            email = usr+"@gmail.com"
            password = "password"+str(i)
            user = User(
                email = email,
                password = get_hash(password),
                role = usr_data[1].value
            )
            db_create_one(user)