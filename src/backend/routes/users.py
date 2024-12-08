from flask import current_app as app
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from ..utils import constants
from ..utils.hash import get_hash
from ..models.user import User, add_new
from ..utils.misc import gen_resp_msg
from ..utils.hash import get_hash
from ..utils.user import user_model_to_api_resp
from ..models.user import User
from ..utils.common import db_create_one, db_commit, db_delete_one, db_delete_all
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


def handle_mod_opr():
    identity = get_jwt_identity()
    output, retval = misc.validate_user(constants.USER_ACCESS)
    if not retval:
        return output

    if request.method == 'POST' and request.json:
        if identity.get('role') == constants.USER_ROLE.ADMIN.value and request.json.get('userRole') == constants.USER_ROLE.ADMIN.value and identity.get('username') != request.json.username:
            return output
        elif identity.get('role') == constants.USER_ROLE.STAFF.value and (request.json.get('userRole') == constants.USER_ROLE.ADMIN.value or (request.json.get('userRole') == constants.USER_ROLE.STAFF.value or identity.get('username') != request.json["username"])):
            return output
        elif identity.get('username') != request.json["username"]:
            return output

    return {}


def add_new_wrapper(request, user_level=constants.USER_ROLE.USER):
    if not request.json['email'] or not request.json['username'] or not request.json['password']:
        return False

    return add_new(request.json['email'], request.json['username'], request.json['password'], user_level)


@app.route('/signup', methods=["POST"])
def signup():
    output = {}
    if request.method == 'POST' and request.json and add_new_wrapper(request):
        output[constants.STATUS] = constants.STATUS_RESPONSE.SUCCESS.value
        output[constants.MESSAGE] = constants.SUCCESS_MSG
        return jsonify(output)

    output[constants.STATUS] = constants.STATUS_RESPONSE.FAILURE.value
    output[constants.MESSAGE] = constants.FAILURE_MSG
    return jsonify(output)


@app.route('/login', methods=["POST"])
def login():
    output = {}
    if request.method == 'POST' and request.json:
        jsonData = request.json
        email = jsonData.get('email')
        password = jsonData.get('password')
        if email and password:
            user = User.query.filter((User.email==email) & (User.password==misc.get_hash(password))).first()
            if user:
                access_token = create_access_token(identity=user)
                output[constants.STATUS] = constants.STATUS_RESPONSE.SUCCESS.value
                output[constants.MESSAGE] = constants.SUCCESS_MSG
                output[constants.JWT_TOKEN] = access_token
                return jsonify(output)

    output[constants.STATUS] = constants.STATUS_RESPONSE.FAILURE.value
    output[constants.MESSAGE] = constants.FAILURE_MSG
    return jsonify(output)


@app.route('/update_user', methods=["POST"])
@jwt_required()
def update_user():
    output = handle_mod_opr()
    if output:
        return output

    if request.json and update_info(request.json['email'], request.json['username'], request.json['password']):
        output[constants.STATUS] = constants.STATUS_RESPONSE.SUCCESS.value
        output[constants.MESSAGE] = constants.SUCCESS_MSG
        return jsonify(output)

    output[constants.STATUS] = constants.STATUS_RESPONSE.FAILURE.value
    output[constants.MESSAGE] = constants.FAILURE_MSG
    return jsonify(output)


@app.route('/create_account', methods=["POST"])
@jwt_required()
def create_account():
    output, retval = misc.validate_user(constants.ADMIN_ACCESS)
    if not retval:
        return output

    if request.method == 'POST' and request.json and request.json.get('userRole') and add_new_wrapper(request, request.json.get('userRole')):
        output[constants.STATUS] = constants.STATUS_RESPONSE.SUCCESS.value
        output[constants.MESSAGE] = constants.SUCCESS_MSG
        return jsonify(output)

    output[constants.STATUS] = constants.STATUS_RESPONSE.FAILURE.value
    output[constants.MESSAGE] = constants.FAILURE_MSG
    return jsonify(output)


@app.route('/delete_user', methods=["POST"])
@jwt_required()
def delete_user():
    output = handle_mod_opr()
    if output:
        return output

    if delete_account(request.json.email, request.json.username):
        output[constants.STATUS] = constants.STATUS_RESPONSE.SUCCESS.value
        output[constants.MESSAGE] = constants.SUCCESS_MSG
        return jsonify(output)

    output[constants.STATUS] = constants.STATUS_RESPONSE.FAILURE.value
    output[constants.MESSAGE] = constants.FAILURE_MSG
    return jsonify(output)


@app.route('/get_users', methods=["GET"])
@jwt_required()
def get_all_users():
    identity = get_jwt_identity()
    output, retval = misc.validate_user(constants.STAFF_ACCESS)
    if output:
        return output

    roles = [constants.USER_ROLE.USER]
    if identity.get("role") == constants.USER_ROLE.ADMIN.value:
        roles.append(constants.USER_ROLE.STAFF)

    users = get_users(roles)
    user_dict = []
    for user in users:
        d={}
        d["id"] = user.id
        d["username"] = user.username
        d["email"] = user.email
        d["role"] = user.role.value
        user_dict.append(d)
    output[constants.STATUS] = constants.STATUS_RESPONSE.SUCCESS.value
    output[constants.MESSAGE] = constants.SUCCESS_MSG
    output[constants.DATA] = user_dict

    return jsonify(output)

@app.route('/populate_users', methods=["POST"])
def populate_users():
    response = {}
    response[constants.STATUS] = -1
    response[constants.MESSAGE] = "failed to add users"

    if not app.get("POPULATE_VALUES"):
        return response

    print("Entered populate_users")
    password = "12345"
    failed = []

    usr_rng = [(100, constants.USER_ROLE.USER), (20, constants.USER_ROLE.STAFF), (5, constants.USER_ROLE.ADMIN)]
    for usr_data in usr_rng:
        for i in range(usr_data[0]):
            usr = usr_data[1].value.lower()+str(i)
            email = usr+"@gmail.com"
            if not add_new(email, usr, password, usr_data[1]):
                print("failed to add", usr)
                failed.append(usr)

    response[constants.STATUS] = len(failed)
    response[constants.MESSAGE] = f"failed: {failed}" if len(failed) else "users added successfully"
    return response

@app.route('/remove_users', methods=["POST"])
def remove_users():
    if not app.get("POPULATE_VALUES"):
        return {}, 404

    print("Entered remove_users")
    result = User.query.delete()
    db.session.commit()
    if not result:
        print("No users present")

    response = {}
    response[constants.STATUS] = result!=0
    response[constants.MESSAGE] = f"users deleted successfully: {result}"
    return response

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
