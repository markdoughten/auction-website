from .. import db
from ..utils import constants
from ..utils.hash import get_hash
from dataclasses import dataclass

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username:str = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    role:constants.USER_ROLE = db.Column(db.Enum(constants.USER_ROLE, values_callable=lambda t: [ str(item.value) for item in t]), nullable=False)

    #methods
    def to_dict(self, with_child_rels=False, with_parent_rels=False):
        d={}
        d["id"] = self.id
        d["username"] = self.username
        d["email"] = self.email
        d["password"] = self.password
        d["role"] = self.role.value

        if with_child_rels:
            pass

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
        if with_parent_rels:
            pass
        return d

def add_new(email, username, password, role=constants.USER_ROLE.USER):
    user = User.query.filter((User.email==email) | (User.username==username)).first()
    if (user is None) and email and username and password:
        user = User(username, email, get_hash(password), role)
        db.session.add(user)
        db.session.commit()
        return True

    return False