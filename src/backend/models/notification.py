from dataclasses import dataclass
from .. import db

@dataclass
class Notification(db.Model):
    __tablename__ = 'notification'
    id = db.Column(db.Integer, primary_key=True)
    uid = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.String(255), nullable=True)

    def __repr__(self):
        return f"<Notification {self.id}, UID {self.uid}, Title {self.title}>"

@dataclass
class Alert(db.Model):
    __tablename__ = 'alerts'
    id = db.Column(db.Integer, primary_key=True)
    item_id = db.Column(db.Integer, db.ForeignKey('items.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    def __repr__(self):
        return f"<Alert {self.id}, Item {self.item_id}, User {self.user_id}>"

def create_notification(uid, title, description=None):
    notification = Notification(uid=uid, title=title, description=description)
    db.session.add(notification)
    db.session.commit()
    return notification

def create_alert(item_id, user_id):
    alert = Alert(item_id=item_id, user_id=user_id)
    db.session.add(alert)
    db.session.commit()
    return alert