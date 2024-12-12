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
    try:
        db.session.delete(obj)
        db.session.commit()
    except Exception as e:
        print("Error deleting row in db:", e)
        raise e

def db_delete_all(model):
    sql = delete(model)
    try:
        db.session.execute(sql)
        db.session.commit()
    except Exception as e:
        print("Error deleting rows in db:", e)
        raise e

def db_session():
    return db.session
