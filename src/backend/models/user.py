from .. import db
from ..utils import constants
from ..utils.misc import get_hash
from dataclasses import dataclass

@dataclass
class User(db.Model):
    __tablename__ = 'users'
    id:int = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username:str = db.Column(db.String(80), unique=True, nullable=False)
    email:str = db.Column(db.String(120), unique=True, nullable=False)
    password:str = db.Column(db.String(128), nullable=False)
    role:constants.USER_ROLE = db.Column(db.Enum(constants.USER_ROLE, values_callable=lambda t: [ str(item.value) for item in t]), nullable=False)

    # init not working even with dataclass??
    def __init__(self, username, email, password, role):
        self.username = username
        self.email = email
        self.password = password
        self.role = role

    #Relationships
    a_user = db.relationship("Auctions", back_populates="a_user")
    b_user = db.relationship("Bids", back_populates="b_user")

@dataclass
class UserQuestion(db.Model):
    __tablename__ = 'user_questions'
    id = db.Column(db.Integer, primary_key=True)
    auction_id = db.Column(db.Integer, db.ForeignKey('auctions.id'), nullable=False)
    asker_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    replier_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    question_text = db.Column(db.String(255), nullable=False)
    is_open = db.Column(db.Boolean, nullable=False)

    def __repr__(self):
        return f"<UserQuestion {self.id}, Auction {self.auction_id}, Asker {self.asker_id}>"

@dataclass
class UserAnswer(db.Model):
    __tablename__ = 'user_answers'
    id = db.Column(db.Integer, primary_key=True)
    question_id = db.Column(db.Integer, db.ForeignKey('user_questions.id'), nullable=False)
    replier_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    reply_text = db.Column(db.String(255), nullable=False)

    def __repr__(self):
        return f"<UserAnswer {self.id}, Question {self.question_id}, Replier {self.replier_id}>"

def add_new(email, username, password, role=constants.USER_ROLE.USER):
    user = User.query.filter((User.email==email) | (User.username==username)).first()
    if (user is None) and email and username and password:
        user = User(username, email, get_hash(password), role)
        db.session.add(user)
        db.session.commit()
        return True

    return False


