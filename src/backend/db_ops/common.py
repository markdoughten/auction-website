from .. import db
from sqlalchemy import delete


def db_commit():
    try:
        db.session.commit()
    except Exception as e:
        print("Error committing: ",e)
        raise e


def db_create_one(obj):
    try:
        db.session.add(obj)
        db.session.commit()
    except Exception as e:
        print("Error adding row in db:", e)
        raise e

def db_delete_one(obj):
    db.session.delete(obj)
    db.session.commit()

def db_delete_all(model):
    sql = delete(model)
    db.session.execute(sql)
    db.session.commit()