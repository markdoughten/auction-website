from flask import current_app as app
from ..utils.misc import gen_resp_msg
from ..tools import seed_item_meta, seed_items, seed_users, seed_auctions, seed_bids, seed_qa, seed_alerts



@app.route('/seed/item_meta', methods=["POST"])
def api_seed_item_meta():
    seed_item_meta()
    return gen_resp_msg(200)



@app.route('/seed/items', methods=["POST"])
def api_seed_items():
    seed_items()
    return gen_resp_msg(200)


@app.route('/seed/users', methods=["POST"])
def api_seed_users():
    seed_users()
    return gen_resp_msg(200)


@app.route('/seed/auctions', methods=["POST"])
def api_seed_auctions():
    seed_auctions()
    return gen_resp_msg(200)


@app.route('/seed/bids', methods=["POST"])
def api_seed_bids():
    seed_bids()
    return gen_resp_msg(200)


@app.route('/seed/qa', methods=["POST"])
def api_seed_qa():
    seed_qa()
    return gen_resp_msg(200)


@app.route('/seed/alerts', methods=["POST"])
def api_seed_alerts():
    seed_alerts()
    return gen_resp_msg(200)

