from flask import current_app as app
from ..utils import constants
from ..models import user
from .. import db

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
