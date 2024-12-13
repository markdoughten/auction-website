from .. import db
from ..utils import constants


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(120), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    role:constants.USER_ROLE = db.Column(db.Enum(constants.USER_ROLE, values_callable=lambda t: [ str(item.value) for item in t]), nullable=False)

    #methods
    def to_dict(self, with_child_rels=False, with_parent_rels=False, with_email=False):
        d={}
        d["username"] = self.username
        d["id"] = self.id
        d["role"] = self.role.value
        if with_email:
            d["email"] = self.email # hidden unless asked for!!

        if with_child_rels:
            pass

        if with_parent_rels:
            pass

        return d
