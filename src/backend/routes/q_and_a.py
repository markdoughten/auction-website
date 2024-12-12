from flask import request, jsonify
from flask import current_app as app
from flask_jwt_extended import jwt_required
from ..utils.misc import gen_resp_msg
from ..models.q_and_a import UserQuestion, UserAnswer
from ..utils.db import db_create_one, db_delete_one, db_delete_all, db_commit


@app.route('/questions/<id>', methods=["GET"])
# @jwt_required()
def get_question(id):
    question = UserQuestion.query.filter(UserQuestion.id==id).first()
    if not question:
        return gen_resp_msg(404)

    return jsonify(question.to_dict(True,True))


@app.route('/questions/<id>', methods=["PUT"])
# @jwt_required()
def put_question(id):
    question = UserQuestion.query.filter(UserQuestion.id==id).first()
    if not question:
        return gen_resp_msg(404)

    if not request.json:
       return gen_resp_msg(400)

    reqJson = request.json
    question.question_text = reqJson["questionText"]
    db_commit()

    return jsonify(question.to_dict())


@app.route('/questions/<id>', methods=["DELETE"])
# @jwt_required()
def delete_question(id):
    question = UserQuestion.query.filter(UserQuestion.id==id).first()
    if not question:
        return gen_resp_msg(404)

    try:
        db_delete_one(question)
    except:
        return gen_resp_msg(500)

    return jsonify(question.to_dict()), 200


@app.route('/questions', methods=["GET"])
# @jwt_required()
def get_questions():
    if not request.args:
       return gen_resp_msg(400)

    page = request.args.get("page")
    page = int(page)

    auction_id = request.args.get("auctionId")
    asker_id = request.args.get("askerId")

    questionQuery = UserQuestion.query
    if(auction_id):
        auction_id=int(auction_id)
        questionQuery=questionQuery.filter(UserQuestion.auction_id == auction_id)

    if(asker_id):
        asker_id=int(asker_id)
        questionQuery=questionQuery.filter(UserQuestion.asker_id == asker_id)

    question = questionQuery.paginate(page=page).items
    questionDict = list(map(lambda x:x.to_dict(True,True),question))
    return jsonify(questionDict)


@app.route('/questions', methods=["POST"])
# @jwt_required()
def post_question():
    if not request.json:
       return gen_resp_msg(400)

    reqJson = request.json

    question = UserQuestion(
        auction_id = reqJson["auctionId"],
        asker_id = reqJson["askerId"],
        question_text = reqJson["questionText"]
    )

    try:
        db_create_one(question)
    except:
        return gen_resp_msg(500)

    return jsonify(question.to_dict())


@app.route('/questions', methods=["DELETE"])
# @jwt_required()
def delete_questions():
    try:
        db_delete_all(UserQuestion)
    except Exception as e:
        return gen_resp_msg(500)

    return gen_resp_msg(200)




@app.route('/answers/<id>', methods=["GET"])
# @jwt_required()
def get_answer(id):
    answer = UserAnswer.query.filter(UserAnswer.id==id).first()
    if not answer:
        return gen_resp_msg(404)

    return jsonify(answer.to_dict(True,True))


@app.route('/answers/<id>', methods=["PUT"])
# @jwt_required()
def put_answer(id):
    answer = UserAnswer.query.filter(UserAnswer.id==id).first()
    if not answer:
        return gen_resp_msg(404)

    if not request.json:
       return gen_resp_msg(400)

    reqJson = request.json
    answer.reply_text = reqJson["replyText"]
    db_commit()

    return jsonify(answer.to_dict())


@app.route('/answers/<id>', methods=["DELETE"])
# @jwt_required()
def delete_answer(id):
    answer = UserAnswer.query.filter(UserAnswer.id==id).first()
    if not answer:
        return gen_resp_msg(404)

    try:
        db_delete_one(answer)
    except:
        return gen_resp_msg(500)

    return jsonify(answer.to_dict()), 200


@app.route('/answers', methods=["POST"])
# @jwt_required()
def post_answer():
    if not request.json:
       return gen_resp_msg(400)

    reqJson = request.json

    answer = UserAnswer(
        question_id = reqJson["questionId"],
        replier_id = reqJson["replierId"],
        reply_text = reqJson["replyText"]
    )

    try:
        db_create_one(answer)
    except:
        return gen_resp_msg(500)

    return jsonify(answer.to_dict())
