from .. import db
from ..utils import constants


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

