from .. import db
from ..models.user import User
from ..utils.misc import get_hash
from ..utils import constants



def add_new(email, username, password, role=constants.USER_ROLE.USER):
    user = User.query.filter((User.email==email) | (User.username==username)).first()
    if (user is None) and email and username and password:
        db.session.add(User(username, email, get_hash(password)))
        db.session.commit()
        return True

    return False