from .. import db
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.orm import Mapped
from typing import List
"""
    Add all item related classes here?
"""


class Item(db.Model):
    __tablename__ = 'items'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), unique=True, nullable=False)
    category_id = db.Column(db.Integer, ForeignKey("meta_item_categories.id"), nullable=False )
    subcategory_id = db.Column(db.Float, ForeignKey("meta_item_subcategories.id"), nullable=False)

    #Relationships
    category = relationship("MetaItemCategory")
    subcategory = relationship("MetaItemSubCategory")
    attributes:Mapped[List["ItemAttribute"]] = relationship(back_populates="item")

    def __repr__(self):
        return f"<Item {self.id}, Name {self.name}, Category {self.category_id}, Sub Category {self.subcategory_id}>"


class ItemAttribute(db.Model):
    __tablename__ = 'item_attributes'
    item_id = db.Column(db.Integer, ForeignKey("items.id"))
    attribute_id = db.Column(db.Integer, ForeignKey("meta_item_attributes.id"))
    attribute_value = db.Column(db.String(255))

    #Relationships
    item: Mapped[Item] = relationship(back_populates="attributes")

    def __repr__(self):
        return f"<Item {self.item_id}, Attr_id {self.attribute_id}, Attr_Value {self.attribute_value}>"