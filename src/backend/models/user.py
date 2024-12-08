from .. import db
from ..utils import constants


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    role:constants.USER_ROLE = db.Column(db.Enum(constants.USER_ROLE, values_callable=lambda t: [ str(item.value) for item in t]), nullable=False)

    #Relationships
    # a_user = db.relationship("Auctions", back_populates="a_user")
    # b_user = db.relationship("Bids", back_populates="b_user")

    #methods
    def to_dict(self, with_child_rels=False, with_parent_rels=False):
        d={}
        d["id"] = self.id
        d["email"] = self.email
        d["password"] = self.password
        d["role"] = self.role.value

        if with_child_rels:
            pass

        if with_parent_rels:
            pass

        return d

