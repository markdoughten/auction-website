from flask import request, jsonify
from flask import current_app as app
from flask_jwt_extended import jwt_required
from ..utils.misc import gen_resp_msg
from ..utils.auction import auction_model_to_api_resp, filter_auctions_by_attr
from ..models.auction import Auctions
from ..db_ops.common import db_create_one, db_delete_one, db_delete_all, db_commit
from datetime import datetime

from sqlalchemy.dialects import mysql

@app.route('/auctions/<id>', methods=["GET"])
# @jwt_required()
def get_auction(id):
    auction = Auctions.query.filter(Auctions.id==id).first()
    if not auction:
        return gen_resp_msg(404)
    
    resp = auction_model_to_api_resp(auction)
    return jsonify(resp)


@app.route('/auctions/<id>', methods=["PUT"])
# @jwt_required() 
def put_auction(id):
    auction = Auctions.query.filter(Auctions.id==id).first()
    if not auction:
        return gen_resp_msg(404)
    
    if not request.json:
        return gen_resp_msg(400)
    
    reqJson = request.json
    
    auction.min_price = reqJson["minPrice"]
    auction.closing_time = datetime.strptime(reqJson["closingTime"], '%m/%d/%Y %H:%M:%S')
    db_commit()

    resp = auction_model_to_api_resp(auction)
    return jsonify(resp)


@app.route('/auctions/<id>', methods=["DELETE"])
# @jwt_required() 
def delete_auction(id):
    auction = Auctions.query.filter(Auctions.id==id).first()
    if not auction:
        return gen_resp_msg(404)

    try:
        db_delete_one(auction)
    except:
        return gen_resp_msg(500)

    return jsonify(auction.to_dict()), 200


@app.route('/auctions', methods=["GET"])
# @jwt_required()
def get_auctions():
    if not request.args:
        return gen_resp_msg(400)


    categoryId = request.args.get("categoryId")
    subcategoryId = request.args.get("subcategoryId")
    initialPrice = request.args.get("initialPrice")
    sellerId = request.args.get("sellerId")


    attr_id = request.args.get("attributeId")
    attr_value = request.args.get("attributeValue")

    auctionsQuery = Auctions.query

    if categoryId:
        auctionsQuery = auctionsQuery.filter(Auctions.item.has(category_id=categoryId))

    if subcategoryId:
        auctionsQuery = auctionsQuery.filter(Auctions.item.has(subcategory_id=subcategoryId))

    if initialPrice:
        auctionsQuery = auctionsQuery.filter(Auctions.initial_price==initialPrice)

    if sellerId:
        auctionsQuery = auctionsQuery.filter(Auctions.seller_id == sellerId)

    page = request.args.get("page")
    page = int(page)
    auctions = auctionsQuery.paginate(page=page).items
    auctionsDict = list(map(lambda x:auction_model_to_api_resp(x),auctions))
    
    if attr_id!=None and attr_value!=None:
        itemsDict = filter_auctions_by_attr(itemsDict, int(attr_id), attr_value)

    return jsonify(auctionsDict)


@app.route('/auctions', methods=["POST"])
# @jwt_required()
def post_auction():
    if not request.json:
        return gen_resp_msg(400)
    
    reqJson = request.json
    
    auction = Auctions(
        item_id = reqJson["itemId"],
        seller_id = reqJson["sellerId"],
        initial_price = reqJson["initialPrice"],
        min_increment = reqJson["minIncrement"],
        min_price = reqJson["minPrice"],
        closing_time = datetime.strptime(reqJson["closingTime"], '%m/%d/%Y %H:%M:%S'),
        status="Open"
    )

    try:
        db_create_one(auction)
    except:
        return gen_resp_msg(500)

    return jsonify(auction.to_dict())


@app.route('/auctions', methods=["DELETE"])
# @jwt_required()
def delete_auctions():
    try:
        db_delete_all(Auctions)
    except Exception as e:
        return gen_resp_msg(500)

    return gen_resp_msg(200)


