from .. import db
from sqlalchemy import ForeignKey, PrimaryKeyConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.orm import Mapped
from typing import List
from ..models.item_meta import MetaItemCategory, MetaItemSubCategory
"""
    Add all item related classes here?
"""


class Item(db.Model):
    __tablename__ = 'items'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), unique=True, nullable=False)
    category_id = db.Column(db.Integer, ForeignKey("meta_item_categories.id"), nullable=False )
    subcategory_id = db.Column(db.Integer, ForeignKey("meta_item_subcategories.id"), nullable=False)

    #Relationships
    category:Mapped[MetaItemCategory] = relationship()
    subcategory:Mapped[MetaItemSubCategory] = relationship()
    attributes:Mapped[List["ItemAttribute"]] = relationship(cascade="all, delete")


    #methods
    def __repr__(self):
        return f"<Item {self.id}, Name {self.name}, Category {self.category_id}, Sub Category {self.subcategory_id}>"

    def to_dict(self, with_child_rels=False, with_parent_rels=False):
        d={}
        d["id"] = self.id
        d["categoryId"] = self.category_id
        d["subcategoryId"] = self.subcategory_id
        d["name"] = self.name
        
        if with_child_rels:
            d["meta"] = self.subcategory.to_dict(with_child_rels=True, with_parent_rels=True)
            d["attributes"] = list(map(lambda x:x.to_dict(), self.attributes))
        
        if with_parent_rels:
            pass

        return d

class ItemAttribute(db.Model):
    __tablename__ = 'item_attributes'
    item_id = db.Column(db.Integer, ForeignKey("items.id", ondelete="CASCADE"))
    attribute_id = db.Column(db.Integer, ForeignKey("meta_item_attributes.id", ondelete="CASCADE"))
    attribute_value = db.Column(db.String(255))
    __table_args__ = (PrimaryKeyConstraint('item_id', 'attribute_id', name='_item_attr_pkey'),)

    #Relationships
    item: Mapped[Item] = relationship(back_populates="attributes")

    #methods
    def __repr__(self):
        return f"<Item {self.item_id}, Attr_id {self.attribute_id}, Attr_Value {self.attribute_value}>"

    def to_dict(self, with_child_rels=False, with_parent_rels=False):
        d={}
        d["attributeId"] = self.attribute_id
        d["attributeValue"] = self.attribute_value

        if with_parent_rels:
            d["item"] = self.item.to_dict(with_parent_rels=True)
        
        if with_child_rels:
            pass

        return d