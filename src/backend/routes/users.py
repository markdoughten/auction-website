from flask import request, jsonify
from flask import current_app as app
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from ..utils import constants
from ..utils.misc import get_hash, gen_resp_msg
from ..utils.user import user_model_to_api_resp
from ..models.user import User
from ..db_ops.common import db_create_one, db_commit, db_delete_one, db_delete_all
from .. import jwt


@jwt.user_identity_loader
def user_identity_lookup(user):
    return {"username": user.email, "role": user.role.value}

@app.route('/users/<id>', methods=["GET"])
def get_user(id):
    user = User.query.filter(User.id==id).first()
    if not user:
        return gen_resp_msg(404)
    
    resp = user_model_to_api_resp(user)
    return jsonify(resp)


@app.route('/users/<id>', methods=["PUT"])
def put_user(id):
    user = User.query.filter(User.id==id).first()
    if not user:
        return gen_resp_msg(404)
    
    if not request.json:
        return gen_resp_msg(400)

    reqJson = request.json

    user.email = reqJson["email"]
    user.password = get_hash(reqJson["password"])
    user.role = reqJson["role"]
    db_commit()

    resp = user_model_to_api_resp(user)
    return jsonify(resp)



@app.route('/users/<id>', methods=["DELETE"])
def delete_user(id):
    user = User.query.filter(User.id==id).first()
    if not user:
        return gen_resp_msg(404)
    
    try:
        db_delete_one(user)
    except:
        return gen_resp_msg(500)

    resp = user_model_to_api_resp(user)
    return jsonify(resp)



@app.route('/users', methods=["POST"])
def post_user():
    if not request.json:
        return gen_resp_msg(400)
    
    reqJson = request.json
    user = User(
        email = reqJson["email"],
        password = get_hash(reqJson["password"]),
        role = reqJson["role"]
    )

    try:
        db_create_one(user)
    except:
        return gen_resp_msg(500)

    resp = user_model_to_api_resp(user)
    return jsonify(resp)



@app.route('/users', methods=["GET"])
# @jwt_required()
def get_users():
    if not request.args:
        return gen_resp_msg(400)

    role = request.args.get("role")
    page = request.args.get("page")
    page = int(page)
    userQuery = User.query
    if(role):
        role=role
        userQuery=userQuery.filter(User.role == role)
  
    users = userQuery.paginate(page=page).items
    usersDict = list(map(lambda x:user_model_to_api_resp(x),users))
    return jsonify(usersDict)


@app.route('/users', methods=["DELETE"])
# @jwt_required()
def delete_users():
    try:
        db_delete_all(User)
    except Exception as e:
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


@app.route('/c_account', methods=["POST"])
@jwt_required()
def create_account():
    identity = get_jwt_identity()
    print(identity)
    
    if not request.json:
        return gen_resp_msg(400)
    
    reqJson = request.json
    user = User(
        email = reqJson["email"],
        password = get_hash(reqJson["password"]),
        role = constants.USER_ROLE.STAFF
    )

    try:
        db_create_one(user)
    except:
        return gen_resp_msg(500)

    resp = user_model_to_api_resp(user)
    return jsonify(resp)
