from flask import request, jsonify
from flask import current_app as app
from flask_jwt_extended import jwt_required
from ..utils.misc import gen_resp_msg
from ..models.item_meta import MetaItemCategory
from ..db_ops.common import db_delete_one, db_delete_all, db_commit

@app.route('/item_meta/categories/<id>', methods=["GET"])
# @jwt_required()
def get_category(id):
    item_category = MetaItemCategory.query.filter(MetaItemCategory.id==id).first()
    if not item_category:
        return gen_resp_msg(404)

    return jsonify(item_category.to_dict(True,True))


@app.route('/item_meta/categories/<id>', methods=["PUT"])
# @jwt_required()
def put_category(id):
    item_category = MetaItemCategory.query.filter(MetaItemCategory.id==id).first()
    if not item_category:
        return gen_resp_msg(404)

    if not request.json:
       return gen_resp_msg(400)

    reqJson = request.json
    item_category.category_name = reqJson["categoryName"]
    db_commit()

    return jsonify(item_category.to_dict(True,True))


@app.route('/item_meta/categories/<id>', methods=["DELETE"])
# @jwt_required()
def delete_category(id):
    item_category = MetaItemCategory.query.filter(MetaItemCategory.id==id).first()
    if not item_category:
        return gen_resp_msg(404)

    try:
        db_delete_one(item_category)
    except:
        return gen_resp_msg(500)

    return jsonify(item_category.to_dict()), 200


@app.route('/item_meta/categories', methods=["GET"])
# @jwt_required()
def get_categories():
    if not request.args:
       return gen_resp_msg(400)

    page = request.args.get("page")
    page = int(page)
    categories = MetaItemCategory.query.paginate(page=page).items
    categoriesDict = list(map(lambda x:x.to_dict(True,True),categories))
    return jsonify(categoriesDict)


@app.route('/item_meta/categories', methods=["POST"])
# @jwt_required()
def post_category():
    if not request.json:
       return gen_resp_msg(400)

    reqJson = request.json

    category = MetaItemCategory(
        category_name = reqJson["categoryName"]
    )

    try:
        db_create_one(category)
    except:
        return gen_resp_msg(500)

    return jsonify(category.to_dict())


@app.route('/item_meta/categories', methods=["DELETE"])
# @jwt_required()
def delete_categories():
    try:
        db_delete_all(MetaItemCategory)
    except Exception as e:
        return gen_resp_msg(500)

    return gen_resp_msg(200)
