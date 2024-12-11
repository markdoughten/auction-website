from flask import request, jsonify
from flask import current_app as app
from flask_jwt_extended import jwt_required
from ..utils.misc import gen_resp_msg
from ..models.auction import Bids, Auctions
from ..utils.db import db_create_one, db_delete_one, db_delete_all, db_commit




@app.route('/bids/<id>', methods=["GET"])
# @jwt_required()
def get_bid(id):
    bid = Bids.query.filter(Bids.id==id).first()
    if not bid:
        return gen_resp_msg(404)
    
    return jsonify(bid.to_dict())



@app.route('/bids/<id>', methods=["DELETE"])
# @jwt_required() 
def delete_bid(id):
    bid = Bids.query.filter(Bids.id==id).first()
    if not bid:
        return gen_resp_msg(404)

    try:
        db_delete_one(bid)
    except:
        return gen_resp_msg(500)

    return jsonify(bid.to_dict()), 200


@app.route('/bids', methods=["GET"])
# @jwt_required()
def get_bids():
    if not request.args:
       return gen_resp_msg(400)

    page = request.args.get("page")
    page = int(page)

    auctionId = request.args.get("auctionId")
    sellerId = request.args.get("sellerId")
    bidderId = request.args.get("bidderId")


    bidsQuery = Bids.query

    if auctionId:
        bidsQuery = bidsQuery.filter(Bids.auction_id == auctionId)

    if sellerId:
        bidsQuery = bidsQuery.filter(Bids.auction.has(seller_id=sellerId))

    if bidderId:
        bidsQuery = bidsQuery.filter(Bids.bidder_id == bidderId)

    bids = bidsQuery.paginate(page=page).items
    bidsDict = list(map(lambda x:x.to_dict(),bids))
    return jsonify(bidsDict)


@app.route('/bids', methods=["POST"])
# @jwt_required()
def post_bid():
    if not request.json:
       return gen_resp_msg(400)
    
    reqJson = request.json
    
    bid = Bids(
        auction_id = reqJson["auctionId"],
        bidder_id = reqJson["bidderId"],
        bid_value = reqJson["bidValue"],
        bid_active = True
    )

    try:
        db_create_one(bid)
    except:
        return gen_resp_msg(500)

    return jsonify(bid.to_dict())


@app.route('/bids', methods=["DELETE"])
# @jwt_required()
def delete_bids():
    try:
        db_delete_all(Bids)
    except Exception as e:
        return gen_resp_msg(500)

    return gen_resp_msg(200)


