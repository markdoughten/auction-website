from sqlalchemy.orm import relationship
from sqlalchemy import ForeignKey, UniqueConstraint
from .. import db
from ..models.user import User
from ..utils.user import user_model_to_api_resp
from sqlalchemy.orm import Mapped
from typing import List

class UserQuestion(db.Model):
    __tablename__ = 'user_questions'
    id:int = db.Column(db.Integer, primary_key=True, autoincrement=True)
    auction_id:int = db.Column(db.Integer, ForeignKey("auctions.id", ondelete="CASCADE"), nullable=False)
    asker_id:int = db.Column(db.Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    question_text:str = db.Column(db.Text, nullable=False)

    #Relationships
    asker:Mapped[User] = relationship()
    answers:Mapped[List["UserAnswer"]] = relationship(cascade="all, delete")

    # methods
    def to_dict(self, with_child_rels=False, with_parent_rels=False):
        d = {}
        d["id"] = self.id
        d["auctionId"] = self.auction_id
        d["askerId"] = self.asker_id
        d["questionText"] = self.question_text

        if (with_child_rels):
            d["answers"] = list(map(lambda x:x.to_dict(with_child_rels=True), self.answers))
            d["asker"] = user_model_to_api_resp(self.asker)
            pass

        if (with_parent_rels):
            pass

        return d

class UserAnswer(db.Model):
    __tablename__ = 'user_answers'
    id:int = db.Column(db.Integer, primary_key=True, autoincrement=True)
    question_id:int = db.Column(db.Integer, ForeignKey("user_questions.id", ondelete="CASCADE"), nullable=False)
    replier_id:int = db.Column(db.Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    reply_text:str = db.Column(db.Text, nullable=False)

    #Relationships
    replier:Mapped[User] = relationship()

    # methods
    def to_dict(self, with_child_rels=False, with_parent_rels=False):
        d = {}
        d["id"] = self.id
        d["questionId"] = self.question_id
        d["replierId"] = self.replier_id
        d["replyText"] = self.reply_text

        if (with_child_rels):
            d["replier"] = user_model_to_api_resp(self.replier)
            pass

        if (with_parent_rels):
            pass

        return d


