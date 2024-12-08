from flask import request, jsonify
from flask import current_app as app
from flask_jwt_extended import jwt_required
from ..utils.misc import gen_resp_msg
from ..models.alert import Alert, Notification
from ..db_ops.common import db_create_one, db_delete_one, db_delete_all
from ..utils.alert import alert_model_to_api_resp



@app.route('/alerts/<id>', methods=["GET"])
# @jwt_required()
def get_alert(id):
    alert = Alert.query.filter(Alert.id==id).first()
    if not alert:
        return gen_resp_msg(404)
    resp = alert_model_to_api_resp(alert)
    return jsonify(resp)



@app.route('/alerts/<id>', methods=["DELETE"])
# @jwt_required() 
def delete_alert(id):
    alert = Alert.query.filter(Alert.id==id).first()
    if not alert:
        return gen_resp_msg(404)

    try:
        db_delete_one(alert)
    except:
        return gen_resp_msg(500)

    return jsonify(alert.to_dict()), 200


@app.route('/alerts', methods=["GET"])
# @jwt_required()
def get_alerts():
    if not request.args:
       return gen_resp_msg(400)

    page = request.args.get("page")
    page = int(page)

    userId = request.args.get("userId")


    alertsQuery = Alert.query

    if userId:
        userId = int(userId)
        alertsQuery =alertsQuery.filter(Alert.user_id == userId)

    alerts = alertsQuery.paginate(page=page).items
    alertsDict = list(map(lambda x:alert_model_to_api_resp(x),alerts))
    return jsonify(alertsDict)


@app.route('/alerts', methods=["POST"])
# @jwt_required()
def post_alert():
    if not request.json:
       return gen_resp_msg(400)
    
    reqJson = request.json
    
    alert = Alert(
        user_id = reqJson["userId"],
        category_id = reqJson["categoryId"],
        subcategory_id = reqJson["subcategoryId"],
        attribute_id = reqJson["attributeId"],
        attribute_value = reqJson["attributeValue"]
    )

    try:
        db_create_one(alert)
    except:
        return gen_resp_msg(500)

    return jsonify(alert.to_dict())


@app.route('/alerts', methods=["DELETE"])
# @jwt_required()
def delete_alerts():
    try:
        db_delete_all(Alert)
    except Exception as e:
        return gen_resp_msg(500)

    return gen_resp_msg(200)



@app.route('/alerts/<id>', methods=["GET"])
# @jwt_required()
def get_notification(id):
    notification = Notification.query.filter(Notification.id==id).first()
    if not notification:
        return gen_resp_msg(404)
    
    return jsonify(notification.to_dict())



@app.route('/notifications', methods=["GET"])
# @jwt_required()
def get_notifications():
    if not request.args:
       return gen_resp_msg(400)

    page = request.args.get("page")
    page = int(page)

    userId = request.args.get("userId")

    notifQuery = Notification.query

    if userId:
        userId = int(userId)
        notifQuery =notifQuery.filter(Notification.user_id == userId)

    notifs = notifQuery.paginate(page=page).items
    notifsDict = list(map(lambda x:x.to_dict(True, True),notifs))
    return jsonify(notifsDict)

