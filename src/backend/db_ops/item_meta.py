from .. import db
from ..models.item_meta import MetaItemCategory


def create_meta_item_category(model:MetaItemCategory):
    try:
        db.session.add(model)
        db.session.commit()
    except Exception as e:
        print("Error adding meta item category in db:", e)
        raise e





