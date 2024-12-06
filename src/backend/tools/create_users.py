from flask import current_app as app
from ..utils import constants
from ..models import user
from .. import db
from idlelib import query

@app.route('/populate_users', methods=["POST"])
def populate_users():
    print("Entered populate_users")
    password = "12345"
    reponse = {}
    failed = []

    for i in range(100):
        email = "user%d@gmail.com" % i
        usr = "user%d" % i
        if not user.add_new(email, usr, password, constants.USER_ROLE.USER):
            failed.append(usr)

    for i in range(20):
        email = "staff%d@gmail.com" % i
        usr = "staff%d" % i
        if not user.add_new(email, usr, password, constants.USER_ROLE.STAFF):
            failed.append(usr)

    for i in range(5):
        email = "admin%d@gmail.com" % i
        usr = "admin%d" % i
        if not user.add_new(email, usr, password, constants.USER_ROLE.ADMIN):
            failed.append(usr)

    reponse[constants.STATUS] = len(failed)
    if len(failed):
        reponse[constants.MESSAGE] = f"failed: {failed}"
    else:
        reponse[constants.MESSAGE] = "users added successfully"

    return reponse


@app.route('/remove_users', methods=["POST"])
def remove_users():
    print("Entered remove_users")
    result = user.User.query.delete()
    db.session.commit()
    return {constants.STATUS: result!=0, constants.MESSAGE: result}
