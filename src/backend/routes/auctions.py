from flask import request, jsonify
from flask import current_app as app
from flask_jwt_extended import jwt_required
from sqlalchemy import delete
from ..utils import constants
from ..utils.misc import gen_resp_msg
from ..models.auction import Auctions
from ..db_ops.common import db_create_one, db_delete_one, db_delete_all, db_commit
from datetime import datetime



@app.route('/auctions/<id>', methods=["GET"])
# @jwt_required()
def get_auction(id):
    auction = Auctions.query.filter(Auctions.id==id).first()
    if not auction:
        return gen_resp_msg(404)
    
    return jsonify(auction.to_dict(True,True))


@app.route('/auctions/<id>', methods=["PUT"])
# @jwt_required() 
def put_auction(id):
    auction = Auctions.query.filter(Auctions.id==id).first()
    if not auction:
        return gen_resp_msg(404)
    
    if not request.json:
        return gen_resp_msg(400)
    
    reqJson = request.json
    
    auction.category_name = reqJson["categoryName"]
    db_commit()

    return jsonify(auction.to_dict(True,True))


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

    attr_id = request.args.get("attributeId")
    attr_value = request.args.get("attributeValue")

    auctionsQuery = Auctions.query

    if categoryId:
        auctionsQuery = auctionsQuery.filter(Auctions.item.has(category_id=categoryId))

    if subcategoryId:
        auctionsQuery = auctionsQuery.filter(Auctions.item.has(subcategory_id=subcategoryId))

    if initialPrice:
        auctionsQuery = auctionsQuery.filter(Auctions.item.has(initial_price=initialPrice))



    page = request.args.get("page")
    page = int(page)
    auctions = auctionsQuery.paginate(page=page).items
    auctionsDict = list(map(lambda x:x.to_dict(True,True),auctions))
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



