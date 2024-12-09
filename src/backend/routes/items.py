from flask import request, jsonify
from flask import current_app as app
from flask_jwt_extended import jwt_required
from ..utils.item import item_model_to_api_resp, filter_items_by_attr
from ..utils.misc import gen_resp_msg
from ..models.item import Item, ItemAttribute
from ..db_ops.common import db_delete_one, db_delete_all, db_commit

@app.route('/items/<id>', methods=["GET"])
# @jwt_required()
def get_item(id):
    item = Item.query.filter(Item.id==id).first()
    if not item:
        return gen_resp_msg(404)

    resp = item_model_to_api_resp(item)

    return jsonify(resp)


@app.route('/items/<id>', methods=["PUT"])
# @jwt_required()
def put_item(id):
    item:Item = Item.query.filter(Item.id==id).first()
    if not item:
        return gen_resp_msg(404)

    if not request.json:
        return gen_resp_msg(400)

    reqJson = request.json


    item.name = reqJson["name"]
    db_commit()

    attr_id_to_val={}
    for attr in reqJson["attributes"]:
        attr_id_to_val[attr["attributeId"]] = attr["attributeValue"]

    for attr in item.attributes:
        attr.attribute_value = attr_id_to_val[attr.attribute_id]
    db_commit()

    resp = item_model_to_api_resp(item)

    return jsonify(resp)


@app.route('/items/<id>', methods=["DELETE"])
# @jwt_required()
def delete_item(id):
    item = Item.query.filter(Item.id==id).first()
    if not item:
        return gen_resp_msg(404)

    try:
        db_delete_one(item)
    except:
        return gen_resp_msg(500)

    return jsonify(item.to_dict()), 200


@app.route('/items', methods=["GET"])
# @jwt_required()
def get_items():
    if not request.args:
        return gen_resp_msg(400)

    categoryId = request.args.get("categoryId")
    subcategoryId = request.args.get("subcategoryId")
    attr_id = request.args.get("attributeId")
    attr_value = request.args.get("attributeValue")

    page = request.args.get("page")
    page = int(page)
    itemQuery = Item.query
    if(categoryId):
        categoryId=int(categoryId)
        itemQuery=itemQuery.filter(Item.category_id == categoryId)

    if(subcategoryId):
        subcategoryId=int(subcategoryId)
        itemQuery=itemQuery.filter(Item.subcategory_id == subcategoryId)


    items = itemQuery.paginate(page=page).items
    itemsDict = list(map(lambda x:item_model_to_api_resp(x),items))

    if attr_id!=None and attr_value!=None:
        itemsDict = filter_items_by_attr(itemsDict, int(attr_id), attr_value)

    return jsonify(itemsDict)


@app.route('/items', methods=["POST"])
# @jwt_required()
def post_item():
    if not request.json:
        return gen_resp_msg(400)

    reqJson = request.json

    item = Item(
        category_id = reqJson["categoryId"],
        subcategory_id = reqJson["subcategoryId"],
        name = reqJson["name"]
    )

    try:
        db_create_one(item)
    except:
        return gen_resp_msg(500)

    for attr in reqJson["attributes"]:
        attribute = ItemAttribute(
            item_id = item.id,
            attribute_id = attr["attributeId"],
            attribute_value = attr["attributeValue"]
            )
        db_create_one(attribute)

    resp = item_model_to_api_resp(item)
    return jsonify(resp)


@app.route('/items', methods=["DELETE"])
# @jwt_required()
def delete_items():
    try:
        db_delete_all(Item)
    except Exception as e:
        return gen_resp_msg(500)

    return gen_resp_msg(200)
