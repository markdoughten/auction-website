from flask import request, jsonify
from flask import current_app as app
from flask_jwt_extended import jwt_required
from sqlalchemy import delete
from ..utils import constants
from ..models.item_meta import MetaItemCategory
from ..models.item_meta import create_new_item, add_item_categ, add_item_attr, MetaItemCategory, MetaItemSubCategory, MetaItemAttribute
from ..db_ops.common import delete_one, delete_all, db_commit
from ..utils import constants
from ..models import item_meta
import os
import json

@app.route('/item_meta/categories/<id>', methods=["GET"])
# @jwt_required()
def get_category(id):
    item_category = MetaItemCategory.query.filter(MetaItemCategory.id==id).first()
    if not item_category:
        output={}
        output[constants.STATUS] = constants.STATUS_RESPONSE.FAILURE.value
        output[constants.MESSAGE] = constants.NOT_FOUND
        return jsonify(output), 404
    
    return jsonify(item_category)

@app.route('/item_meta/categories/<id>', methods=["PUT"])
# @jwt_required() 
def put_category(id):
    item_category = MetaItemCategory.query.filter(MetaItemCategory.id==id).first()
    if not item_category:
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
    
    item_category.category_name = reqJson["categoryName"]
    db_commit()

    return jsonify(item_category)

@app.route('/item_meta/categories/<id>', methods=["DELETE"])
# @jwt_required() 
def delete_category(id):
    item_category = MetaItemCategory.query.filter(MetaItemCategory.id==id).first()
    if not item_category:
        output={}
        output[constants.STATUS] = constants.STATUS_RESPONSE.FAILURE.value
        output[constants.MESSAGE] = constants.NOT_FOUND
        return jsonify(output), 404

    try:
        delete_one(item_category)
    except:
        output ={}
        output[constants.STATUS] = constants.STATUS_RESPONSE.FAILURE.value
        output[constants.MESSAGE] = constants.FAILURE_MSG
        return jsonify(output), 400

    return jsonify(item_category), 200


@app.route('/item_meta/categories', methods=["GET"])
# @jwt_required()
def get_categories():
    if not request.args:
        output={}
        output[constants.STATUS] = constants.STATUS_RESPONSE.FAILURE.value
        output[constants.MESSAGE] = constants.INVALID_REQ
        return jsonify(output), 401

    page = request.args.get("page")
    page = int(page)
    categories = MetaItemCategory.query.paginate(page=page).items
    return jsonify(categories)

@app.route('/item_meta/categories', methods=["POST"])
# @jwt_required()
def post_category():
    if not request.json:
        output={}
        output[constants.STATUS] = constants.STATUS_RESPONSE.FAILURE.value
        output[constants.MESSAGE] = constants.INVALID_REQ
        return jsonify(output), 401
    
    reqJson = request.json
    
    category = MetaItemCategory(
        category_name = reqJson["categoryName"]
    )

    try:
        add_item_categ(category)
    except:
        output ={}
        output[constants.STATUS] = constants.STATUS_RESPONSE.FAILURE.value
        output[constants.MESSAGE] = constants.FAILURE_MSG
        return jsonify(output), 400

    return jsonify(category)

@app.route('/item_meta/categories', methods=["DELETE"])
# @jwt_required()
def delete_categories():
    try:
        delete_all(MetaItemCategory)
        output ={}
        output[constants.STATUS] = constants.STATUS_RESPONSE.SUCCESS.value
        output[constants.MESSAGE] = constants.SUCCESS_MSG
        return jsonify(output), 200
    except Exception as e:
        output ={}
        output[constants.STATUS] = constants.STATUS_RESPONSE.FAILURE.value
        output[constants.MESSAGE] = constants.FAILURE_MSG
        return jsonify(output), 400