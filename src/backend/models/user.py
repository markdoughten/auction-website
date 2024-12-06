from .. import db
from ..utils import constants
from ..utils.misc import get_hash



class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    role = db.Column(db.Enum(constants.USER_ROLE, values_callable=lambda t: [ str(item.value) for item in t]), nullable=False)

    def __init__(self, username, email, password, role=constants.USER_ROLE.USER):
        self.username = username
        self.email = email
        self.password = password
        self.role = role

    def __repr__(self):
        return f"<User {self.id}, Name {self.username}, Email {self.email}, Role {self.role}>"
    


def add_new(email, username, password, role=constants.USER_ROLE.USER):
    user = User.query.filter((User.email==email) | (User.username==username)).first()
    if (user is None) and email and username and password:
        db.session.add(User(username, email, get_hash(password)))
        db.session.commit()
        return True

    return False