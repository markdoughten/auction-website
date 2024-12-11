from ..models.q_and_a import UserQuestion, UserAnswer
from ..utils.db import db_create_one


def seed_qa():
    for auction_id in range(1,7):
        asker_id =  auction_id*10
        question_text = "question text " + str(asker_id) + "?"
        ques = UserQuestion(
            auction_id = auction_id,
            asker_id = asker_id,
            question_text = question_text
        )
        db_create_one(ques)

        for replier_id in range(101,105):
            reply_text = "Reply " + str(replier_id)
            ans = UserAnswer(
                question_id = ques.id,
                replier_id = replier_id,
                reply_text = reply_text
            )
            db_create_one(ans)