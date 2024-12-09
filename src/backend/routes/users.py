from flask import current_app as app, request
from flask.json import jsonify
from flask_jwt_extended import create_access_token, jwt_required
from flask_jwt_extended.utils import get_jwt_identity

from ..utils import constants
from ..utils.hash import get_hash
from ..utils.misc import gen_resp_msg, gen_success_response
from ..utils.user import user_model_to_api_resp, is_opr_allowed
from ..models.user import User
from ..models.auction import Auctions, Bids
from ..db_ops.common import db_create_one, db_commit, db_delete_one, db_delete_all, db_session
from .. import jwt



@jwt.user_identity_loader
def user_identity_lookup(user: User):
    return {"id": user.id, "username": user.username, "email": user.email, "role": user.role.value}



@app.route('/users/<id>', methods=["GET"])
def get_user(id):
    user = User.query.filter(User.id==id).first()
    if not user:
        return gen_resp_msg(404)

    return gen_success_response(user_model_to_api_resp(user))



@app.route('/users/<id>', methods=["PUT"])
@jwt_required()
def put_user(id):
    if not is_opr_allowed(constants.USER_ACCESS):
        return gen_resp_msg(403)

    user = User.query.filter(User.id==id).first()
    if not user:
        return gen_resp_msg(404)

    if not request.json:
        return gen_resp_msg(400)

    reqJson = request.json
    if (reqJson["email"] != user.email):
        user.email = reqJson["email"]
    if (reqJson["role"] != reqJson["role"]):
        user.role = reqJson["role"]
    user.password = get_hash(reqJson["password"])
    db_commit()

    return gen_success_response(user_model_to_api_resp(user))



@app.route('/users/<id>', methods=["DELETE"])
@jwt_required()
def delete_user(id):
    print(id)
    if not is_opr_allowed(constants.USER_ACCESS):
        return gen_resp_msg(403)

    user = User.query.filter(User.id==id).first()
    if not user:
        return gen_resp_msg(404)

    try:
        db_delete_one(user)
    except:
        return gen_resp_msg(500)

    return gen_success_response(user_model_to_api_resp(user))



@app.route('/users', methods=["POST"])
def post_user():
    if not request.json:
        return gen_resp_msg(400)

    reqJson = request.json
    user = User(
        username = reqJson["username"],
        email = reqJson["email"],
        password = get_hash(reqJson["password"]),
        role = constants.USER_ROLE.USER
    )

    try:
        db_create_one(user)
    except:
        return gen_resp_msg(500)

    return gen_success_response(user_model_to_api_resp(user))



@app.route('/users', methods=["GET"])
@jwt_required()
def get_users():
    identity = get_jwt_identity()
    if not identity or not is_opr_allowed(constants.STAFF_ACCESS):
        return gen_resp_msg(403)

    role = [constants.USER_ROLE.USER]
    if identity.get('role') == constants.USER_ROLE.ADMIN:
        role.append(constants.USER_ROLE.STAFF)

    # page = request.args.get("page")
    # page = int(page)
    userQuery = User.query
    if(role):
        role=role
        userQuery=userQuery.filter(User.role.in_(role))

    # users = userQuery.paginate(page=page).items
    users = userQuery.all()
    usersDict = list(map(lambda x:user_model_to_api_resp(x),users))
    return gen_success_response(usersDict)


@app.route('/users', methods=["DELETE"])
@jwt_required()
def delete_users():
    return gen_resp_msg(403) # disable this for now

    try:
        db_delete_all(User)
    except Exception:
        return gen_resp_msg(500)

    return gen_resp_msg(200)


@app.route('/user/login', methods=["POST"])
def login():
    if not request.json:
        return gen_resp_msg(400)

    jsonData = request.json
    email = jsonData.get('email')
    password = jsonData.get('password')

    if not email or not password:
        return gen_resp_msg(400)

    user = User.query.filter(User.email==email, User.password==get_hash(password)).first()
    print(user)
    if not user:
        return gen_resp_msg(404)

    access_token = create_access_token(identity=user)
    output = {}
    output[constants.STATUS] = constants.STATUS_RESPONSE.SUCCESS.value
    output[constants.MESSAGE] = constants.SUCCESS_MSG
    output[constants.JWT_TOKEN] = access_token
    return jsonify(output)


@app.route('/users/items/<id>', methods=["GET"])
def get_user_items(id):
    items = Auctions.query.filter(Auctions.seller_id==id).all()
    if not items:
        return gen_resp_msg(404)

    items_dict = [item.to_dict(with_parent_rels=True) for item in items]
    print(items_dict)
    return gen_success_response(items_dict)


@app.route('/users/bids/<id>', methods=["GET"])
def get_user_bids(id):
    bids = Bids.query.filter(Bids.users_id==id).all()
    if not bids:
        return gen_resp_msg(404)

    bid_dict = [bid.to_dict(False, True) for bid in bids]
    print(bid_dict)
    return gen_success_response(bid_dict)


@app.route('/c_account', methods=["POST"])
@jwt_required()
def create_account():
    identity = get_jwt_identity()
    if not identity or identity.get('role') not in constants.ADMIN_ACCESS:
        return gen_resp_msg(403)

    if not request.json:
        return gen_resp_msg(400)

    reqJson = request.json
    user = User(
        username = reqJson["username"],
        email = reqJson["email"],
        password = get_hash(reqJson["password"]),
        role = reqJson["role"]
    )

    try:
        db_create_one(user)
    except:
        return gen_resp_msg(500)

    return gen_success_response(user_model_to_api_resp(user))
