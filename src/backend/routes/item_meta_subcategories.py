from flask import request, jsonify
from flask import current_app as app
from flask_jwt_extended import jwt_required
from ..utils.misc import gen_resp_msg
from ..models.item_meta import MetaItemSubCategory
from ..utils.common import db_delete_one, db_delete_all, db_commit


@app.route('/item_meta/subcategories/<id>', methods=["GET"])
# @jwt_required()
def get_subcategory(id):
    item_subcategory = MetaItemSubCategory.query.filter(MetaItemSubCategory.id==id).first()
    if not item_subcategory:
        return gen_resp_msg(404)
    
    return jsonify(item_subcategory.to_dict(True, True))

@app.route('/item_meta/subcategories/<id>', methods=["PUT"])
# @jwt_required() 
def put_subcategory(id):
    item_subcategory = MetaItemSubCategory.query.filter(MetaItemSubCategory.id==id).first()
    if not item_subcategory:
        return gen_resp_msg(404)
    
    if not request.json:
        return gen_resp_msg(400)
    
    reqJson = request.json
    
    item_subcategory.subcategory_name = reqJson["subcategoryName"]
    db_commit()

    return jsonify(item_subcategory.to_dict(True, True))


@app.route('/item_meta/subcategories/<id>', methods=["DELETE"])
# @jwt_required() 
def delete_subcategory(id):
    item_subcategory = MetaItemSubCategory.query.filter(MetaItemSubCategory.id==id).first()
    if not item_subcategory:
        return gen_resp_msg(404)

    try:
        db_delete_one(item_subcategory)
    except:
        return gen_resp_msg(500)

    return jsonify(item_subcategory.to_dict()), 200


@app.route('/item_meta/subcategories', methods=["GET"])
# @jwt_required()
def get_subcategories():
    if not request.args:
        return gen_resp_msg(400)

    page = request.args.get("page")
    page = int(page)
    subcategories = MetaItemSubCategory.query.paginate(page=page).items
    subcategoriesDict = list(map(lambda x:x.to_dict(True, True), subcategories))
    return jsonify(subcategoriesDict)


@app.route('/item_meta/subcategories', methods=["POST"])
# @jwt_required()
def post_subcategory():
    if not request.json:
        return gen_resp_msg(400)
    
    reqJson = request.json
    
    subcategory = MetaItemSubCategory(
        subcategory_name = reqJson["subcategoryName"],
        category_id = reqJson["categoryId"]
    )

    try:
        db_create_one(subcategory)
    except:
        return gen_resp_msg(500)

    return jsonify(subcategory.to_dict())


@app.route('/item_meta/subcategories', methods=["DELETE"])
# @jwt_required()
def delete_subcategories():
    try:
        db_delete_all(MetaItemSubCategory)
    except Exception as e:
        return gen_resp_msg(500)

    return gen_resp_msg(200)


