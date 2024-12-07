from .. import db
from sqlalchemy import delete

def db_commit():
    db.session.commit()

def delete_one(obj):
    db.session.delete(obj)
    db.session.commit()

def delete_all(model):
    sql = delete(model)
    db.session.execute(sql)
    db.session.commit()