from flask import request, jsonify
from flask import current_app as app
from flask_jwt_extended import (create_access_token, jwt_required, get_jwt_identity)
from ..utils import constants
from ..utils.misc import get_hash
from ..models.user import User, add_new
from .. import jwt

@jwt.user_identity_loader
def user_identity_lookup(user):
    return {"username": user.username, "role": user.role.value}

def add_new_wrapper(request, user_level=constants.USER_ROLE.USER):
    return add_new(request.json.get('email'), request.json.get('uname'), request.json.get('password'), user_level)

@app.route('/populate_users', methods=["POST"])
def populate_users():
    print("Entered populate_users")
    password = "12345"
    failed = []

    usr_rng = [(100, constants.USER_ROLE.USER), (20, constants.USER_ROLE.STAFF), (5, constants.USER_ROLE.ADMIN)]
    for usr_data in usr_rng:
        for i in range(usr_data[0]):
            usr = usr_data[1].value.lower()+str(i)
            email = usr+"@gmail.com"
            if not user.add_new(email, usr, password, usr_data[1]):
                print("failed to add", usr)
                failed.append(usr)

    response = {}
    response[constants.STATUS] = len(failed)
    response[constants.MESSAGE] = f"failed: {failed}" if len(failed) else "users added successfully"
    return response

@app.route('/remove_users', methods=["POST"])
def remove_users():
    print("Entered remove_users")
    result = user.User.query.delete()
    db.session.commit()
    if not result:
        print("No users present")

    response = {}
    response[constants.STATUS] = result!=0
    response[constants.MESSAGE] = f"users deleted successfully: {result}"
    return response