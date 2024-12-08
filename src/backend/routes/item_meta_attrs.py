from flask import request, jsonify
from flask import current_app as app
from flask_jwt_extended import jwt_required
from ..utils.misc import gen_resp_msg
from ..models.item_meta import MetaItemAttribute
from ..db_ops.common import db_create_one, db_delete_one, db_delete_all, db_commit




@app.route('/item_meta/attributes/<id>', methods=["GET"])
# @jwt_required()
def get_attr(id):
    item_attr = MetaItemAttribute.query.filter(MetaItemAttribute.id==id).first()
    if not item_attr:
        return gen_resp_msg(404)
    
    return jsonify(item_attr.to_dict(True, True))


@app.route('/item_meta/attributes/<id>', methods=["PUT"])
# @jwt_required() 
def put_attr(id):
    item_attr = MetaItemAttribute.query.filter(MetaItemAttribute.id==id).first()
    if not item_attr:
        return gen_resp_msg(404)
    
    if not request.json:
        return gen_resp_msg(400)
    
    reqJson = request.json
    
    item_attr.attribute_name = reqJson["attributeName"]
    db_commit()

    return jsonify(item_attr.to_dict(True, True))


@app.route('/item_meta/attributes/<id>', methods=["DELETE"])
# @jwt_required() 
def delete_attr(id):
    item_attr = MetaItemAttribute.query.filter(MetaItemAttribute.id==id).first()
    if not item_attr:
        return gen_resp_msg(404)

    try:
        db_delete_one(item_attr)
    except:
        return gen_resp_msg(500)

    return jsonify(item_attr.to_dict()), 200


@app.route('/item_meta/attributes', methods=["GET"])
# @jwt_required()
def get_attributes():
    if not request.args:
        return gen_resp_msg(400)

    page = request.args.get("page")
    page = int(page)
    attributes = MetaItemAttribute.query.paginate(page=page).items
    attributesDict = list(map(lambda x:x.to_dict(True, True), attributes))
    return jsonify(attributesDict)


@app.route('/item_meta/attributes', methods=["POST"])
# @jwt_required()
def post_attr():
    if not request.json:
        return gen_resp_msg(400)
    
    reqJson = request.json
    
    attribute = MetaItemAttribute(
        attribute_name = reqJson["attributeName"],
        subcategory_id = reqJson["subcategoryId"]
    )

    try:
        db_create_one(attribute)
    except:
        return gen_resp_msg(500)

    return jsonify(attribute.to_dict())


@app.route('/item_meta/attributes', methods=["DELETE"])
# @jwt_required()
def delete_attributes():
    try:
        db_delete_all(MetaItemAttribute)
    except Exception as e:
        return gen_resp_msg(500)

    return gen_resp_msg(200)


