from flask.json import jsonify
from sqlalchemy import func
from flask import current_app as app
from flask_jwt_extended import get_jwt_identity, jwt_required
from flask_csv import send_csv

from ..utils.db import db_session
from ..utils.constants import ADMIN_ACCESS
from ..utils.misc import gen_resp_msg
from ..models.auction import Bids, Auctions
from ..models.item import Item

@app.route('/get_report/<opr>', methods=["POST"])
@jwt_required()
def get_report(opr):
    identity = get_jwt_identity()
    if not identity or identity.get('role') not in ADMIN_ACCESS:
        return gen_resp_msg(403)

    profits = None
    if opr == "get_profit":
        output = db_session().query(Bids.id, func.max(Bids.bid_value)).filter(Bids.auction_id==Auctions.id).group_by(Bids.id)
        profits = {"profit": output}
        return send_csv(profits, "profits.csv", ["profits"])
    elif opr == "usr_sales":
        output = db_session().query(Bids.users_id, func.sum(Bids.bid_value)).filter(Bids.bid_active==True).group_by(Bids.users_id).all()
        profits = []
        for profit in output:
            print(profit)
            # profits.append({
            #     "user_id": profit.id,
            #     "bid_value": profit.bid_value
            # })
        return send_csv(profits, "profits.csv", ["user_id", "bid_value"])
    elif opr == "itm_sales":
        output = db_session().query(Auctions.item_id, func.sum(Bids.bid_value)).filter(Bids.bid_active==True & Bids.auction_id==Auctions.id).group_by(Auctions.item_id).all()
        profits = []
        for profit in output:
            print(profit)
            # profits.append({
            #     "item_id": profit.item_id,
            #     "bid_value": profit.bid_value
            # })
        return send_csv(profits, "profits.csv", ["item_id", "bid_value"])
    elif opr == "itm_type":
        output = db_session().query(Item.category_id, func.sum(Bids.bid_value)).filter(Bids.bid_active==True & Bids.auction_id==Auctions.id & Bids.auction_id==Auctions.id & Auctions.item_id==Item.id).group_by(Item.category_id).all()
        profits = []
        for profit in output:
            print(profit)
            # profits.append({
            #     "category_id": profit.category_id,
            #     "bid_value": profit.bid_value
            # })
        return send_csv(profits, "profits.csv", ["category_id", "bid_value"])
    # elif opr == "best_usrs":
    #     profits = db_session().query(Bids.user_id, func.sum(Bids.bid_value)).filter(Bids.bid_active==True).group_by(Bids.user_id).all()
    # elif opr == "best_itms":
    #     profits = db_session().query(Bids.user_id, func.sum(Bids.bid_value)).filter(Bids.bid_active==True).group_by(Bids.user_id).all()
    else:
        gen_resp_msg(400)

    if profits:
        return jsonify(profits)
    else:
        return gen_resp_msg(404)

    # output, retval = misc.validate_user(constants.ADMIN_ACCESS)
    # if not retval:
    #     return output
