from .. import db

"""
    Add all item related classes here?
"""

class Item(db.Model):
    __tablename__ = 'items'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), unique=True, nullable=False)
    category_id = db.Column(db.Integer, nullable=False)
    subcategory_id = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return f"<Item {self.id}, Name {self.name}, Category {self.category_id}, Sub Category {self.subcategory_id}>"