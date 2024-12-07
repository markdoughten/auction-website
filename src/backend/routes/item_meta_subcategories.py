from flask import request, jsonify
from flask import current_app as app
from flask_jwt_extended import jwt_required
from sqlalchemy import delete
from ..utils import constants
from ..models.item_meta import MetaItemSubCategory
from ..db_ops.common import db_create_one, db_delete_one, db_delete_all, db_commit


@app.route('/item_meta/subcategories/<id>', methods=["GET"])
# @jwt_required()
def get_subcategory(id):
    item_subcategory = MetaItemSubCategory.query.filter(MetaItemSubCategory.id==id).first()
    if not item_subcategory:
        output={}
        output[constants.STATUS] = constants.STATUS_RESPONSE.FAILURE.value
        output[constants.MESSAGE] = constants.NOT_FOUND
        return jsonify(output), 404
    
    return jsonify(item_subcategory.to_dict(True, True))


@app.route('/item_meta/subcategories/<id>', methods=["PUT"])
# @jwt_required() 
def put_subcategory(id):
    item_subcategory = MetaItemSubCategory.query.filter(MetaItemSubCategory.id==id).first()
    if not item_subcategory:
        output={}
        output[constants.STATUS] = constants.STATUS_RESPONSE.FAILURE.value
        output[constants.MESSAGE] = constants.NOT_FOUND
        return jsonify(output), 404
    
    if not request.json:
        output={}
        output[constants.STATUS] = constants.STATUS_RESPONSE.FAILURE.value
        output[constants.MESSAGE] = constants.INVALID_REQ
        return jsonify(output), 401
    
    reqJson = request.json
    
    item_subcategory.subcategory_name = reqJson["subcategoryName"]
    db_commit()

    return jsonify(item_subcategory.to_dict(True, True))


@app.route('/item_meta/subcategories/<id>', methods=["DELETE"])
# @jwt_required() 
def delete_subcategory(id):
    item_subcategory = MetaItemSubCategory.query.filter(MetaItemSubCategory.id==id).first()
    if not item_subcategory:
        output={}
        output[constants.STATUS] = constants.STATUS_RESPONSE.FAILURE.value
        output[constants.MESSAGE] = constants.NOT_FOUND
        return jsonify(output), 404

    try:
        db_delete_one(item_subcategory)
    except:
        output ={}
        output[constants.STATUS] = constants.STATUS_RESPONSE.FAILURE.value
        output[constants.MESSAGE] = constants.FAILURE_MSG
        return jsonify(output), 400

    return jsonify(item_subcategory.to_dict()), 200


@app.route('/item_meta/subcategories', methods=["GET"])
# @jwt_required()
def get_subcategories():
    if not request.args:
        output={}
        output[constants.STATUS] = constants.STATUS_RESPONSE.FAILURE.value
        output[constants.MESSAGE] = constants.INVALID_REQ
        return jsonify(output), 401

    page = request.args.get("page")
    page = int(page)
    subcategories = MetaItemSubCategory.query.paginate(page=page).items
    subcategoriesDict = list(map(lambda x:x.to_dict(True, True), subcategories))
    return jsonify(subcategoriesDict)


@app.route('/item_meta/subcategories', methods=["POST"])
# @jwt_required()
def post_subcategory():
    if not request.json:
        output={}
        output[constants.STATUS] = constants.STATUS_RESPONSE.FAILURE.value
        output[constants.MESSAGE] = constants.INVALID_REQ
        return jsonify(output), 401
    
    reqJson = request.json
    
    subcategory = MetaItemSubCategory(
        subcategory_name = reqJson["subcategoryName"],
        category_id = reqJson["categoryId"]
    )

    try:
        db_create_one(subcategory)
    except:
        output ={}
        output[constants.STATUS] = constants.STATUS_RESPONSE.FAILURE.value
        output[constants.MESSAGE] = constants.FAILURE_MSG
        return jsonify(output), 400

    return jsonify(subcategory.to_dict())


@app.route('/item_meta/subcategories', methods=["DELETE"])
# @jwt_required()
def delete_subcategories():
    try:
        db_delete_all(MetaItemSubCategory)
        output ={}
        output[constants.STATUS] = constants.STATUS_RESPONSE.SUCCESS.value
        output[constants.MESSAGE] = constants.SUCCESS_MSG
        return jsonify(output), 200
    except Exception as e:
        output ={}
        output[constants.STATUS] = constants.STATUS_RESPONSE.FAILURE.value
        output[constants.MESSAGE] = constants.FAILURE_MSG
        return jsonify(output), 400




