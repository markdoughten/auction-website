from flask import request, jsonify
from flask import current_app as app
from flask_jwt_extended import jwt_required
from ..utils.misc import gen_resp_msg
from ..utils.auction import auction_model_to_api_resp, filter_auctions_by_attr
from ..models.auction import Auctions
from ..utils.db import db_create_one, db_delete_one, db_delete_all, db_commit
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



@auctions_bp.route("/auctions/<int:auction_id>", methods=["GET", "POST", "PUT", "DELETE"])
@jwt_required()
def manage_auction(auction_id):
    auction = Auctions.query.filter(Auctions.id == auction_id).first()

    if request.method == "GET":
        if not auction:
            return gen_resp_msg(404)
        return gen_success_response(auction_model_to_api_resp(auction))

    elif request.method == "PUT":
        if not auction or not request.json:
            return gen_resp_msg(400)
        req_json = request.json
        auction.min_price = req_json.get("minPrice", auction.min_price)
        auction.closing_time = datetime.strptime(req_json["closingTime"], '%m/%d/%Y %H:%M:%S')
        db_commit()
        return gen_success_response(auction_model_to_api_resp(auction))

    elif request.method == "DELETE":
        if not auction:
            return gen_resp_msg(404)
        db_delete_one(auction)
        return gen_success_response(auction.to_dict())


@auctions_bp.route("/auctions", methods=["GET", "POST", "DELETE"])
@jwt_required()
def handle_auctions():
    if request.method == "GET":
        category_id = request.args.get("categoryId")
        subcategory_id = request.args.get("subcategoryId")
        initial_price = request.args.get("initialPrice")
        seller_id = request.args.get("sellerId")
        attr_id = request.args.get("attributeId")
        attr_value = request.args.get("attributeValue")
        page = int(request.args.get("page", 1))

        auctions_query = Auctions.query
        if category_id:
            auctions_query = auctions_query.filter(Auctions.item.has(category_id=category_id))
        if subcategory_id:
            auctions_query = auctions_query.filter(Auctions.item.has(subcategory_id=subcategory_id))
        if initial_price:
            auctions_query = auctions_query.filter(Auctions.initial_price == initial_price)
        if seller_id:
            auctions_query = auctions_query.filter(Auctions.seller_id == seller_id)

        auctions = auctions_query.paginate(page=page).items
        auctions_dict = [auction_model_to_api_resp(a) for a in auctions]

        if attr_id and attr_value:
            auctions_dict = filter_auctions_by_attr(auctions_dict, int(attr_id), attr_value)

        return jsonify(auctions_dict)

    elif request.method == "POST":
        if not request.json:
            return gen_resp_msg(400)
        req_json = request.json

        auction = Auctions(
            item_id=req_json["itemId"],
            seller_id=req_json["sellerId"],
            initial_price=req_json["initialPrice"],
            min_increment=req_json["minIncrement"],
            min_price=req_json["minPrice"],
            closing_time=datetime.strptime(req_json["closingTime"], '%m/%d/%Y %H:%M:%S'),
            status="Open"
        )

        db_create_one(auction)
        return jsonify(auction.to_dict())

    elif request.method == "DELETE":
        db_delete_all(Auctions)
        return gen_resp_msg(200)


@auctions_bp.route('/add_items', methods=["POST"])
def add_items():
    failed = []
    dir_path = os.path.dirname(os.path.realpath(__file__))
    with open(os.path.join(dir_path, 'dict/meta_items.json')) as f:
        m_itm = json.load(f)
        for item, categs in m_itm.items():
            for categ, attrs in categs.items():
                for attr in attrs:
                    sub_item, retval = item_meta.add_item_attr(item, categ, attr)
                    if sub_item is None or not retval:
                        failed.append((item, categ, attr))

    response = {
        constants.STATUS: len(failed),
        constants.MESSAGE: failed if failed else "Items added successfully"
    }
    return jsonify(response)



@app.route('/all_auctions', methods=["GET"])
def get_all():
    auctions = Auctions.query.filter(Auctions.status == 'Open').all()
    if not auctions:
        return gen_resp_msg(404)

    auction_items = [auction.to_dict() for auction in auctions]
    return gen_success_response(auction_items)
