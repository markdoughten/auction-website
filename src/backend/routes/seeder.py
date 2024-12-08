from flask import current_app as app
from ..utils.misc import gen_resp_msg
from ..tools import seed_item_meta, seed_items, seed_users, seed_auctions, seed_bids



@app.route('/seed/item_meta', methods=["POST"])
def add_item_meta():
    seed_item_meta()
    return gen_resp_msg(200)



@app.route('/seed/items', methods=["POST"])
def add_items():
    seed_items()
    return gen_resp_msg(200)


@app.route('/seed/users', methods=["POST"])
def add_users():
    seed_users()
    return gen_resp_msg(200)


@app.route('/seed/auctions', methods=["POST"])
def add_auctions():
    seed_auctions()
    return gen_resp_msg(200)


@app.route('/seed/bids', methods=["POST"])
def add_bids():
    seed_bids()
    return gen_resp_msg(200)

