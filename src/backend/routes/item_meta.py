from flask import request, jsonify
from flask import current_app as app
from flask_jwt_extended import jwt_required
from ..utils import constants
from ..models.item_meta import MetaItemCategory
from ..db_ops.item_meta import create_meta_item_category




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
    print("1******",category.id)
    try:
        create_meta_item_category(category)
    except:
        output ={}
        output[constants.STATUS] = constants.STATUS_RESPONSE.FAILURE.value
        output[constants.MESSAGE] = constants.FAILURE_MSG
        return jsonify(output), 400

    print("2******",category.id)


    return jsonify(category)
