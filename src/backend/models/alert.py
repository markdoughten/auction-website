from sqlalchemy.orm import relationship
from sqlalchemy import ForeignKey, UniqueConstraint
from .. import db
from ..models.user import User
from ..models.item_meta import MetaItemSubCategory
from ..models.item import Item
from sqlalchemy.orm import Mapped
from typing import List

class Alert(db.Model):
    __tablename__ = 'alerts'
    id:int = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id:int = db.Column(db.Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    category_id:int = db.Column(db.Integer, ForeignKey("meta_item_categories.id", ondelete="CASCADE"), nullable=False)
    subcategory_id:int = db.Column(db.Integer, ForeignKey("meta_item_subcategories.id", ondelete="CASCADE"), nullable=False)
    attribute_id:int = db.Column(db.Integer, ForeignKey("meta_item_attributes.id", ondelete="CASCADE"), nullable=False)
    attribute_value:int = db.Column(db.String(255))

    #Relationships
    subcategory:Mapped[MetaItemSubCategory] = relationship()

    #methods
    def to_dict(self, with_child_rels=False, with_parent_rels=False):
        d={}
        d["id"] = self.id
        d["userId"] = self.user_id
        d["categoryId"] = self.category_id
        d["subcategoryId"] = self.subcategory_id
        d["attributeId"] = self.attribute_id
        d["attributeValue"] = self.attribute_value

        if with_child_rels:
            d["meta"] = self.subcategory.to_dict(with_child_rels=True, with_parent_rels=True)

        if with_parent_rels:
            pass

        return d


class Notification(db.Model):
    __tablename__ = 'notifications'
    id:int = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id:int = db.Column(db.Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    item_id:int = db.Column(db.Integer, ForeignKey("items.id", ondelete="CASCADE"), nullable=False)

    #Relationships
    item:Mapped[Item] = relationship()

    #methods
    def to_dict(self, with_child_rels=False, with_parent_rels=False):
        d={}
        d["id"] = self.id
        d["userId"] = self.user_id
        d["itemId"] = self.item_id

        if with_child_rels:
            d["item"] = self.item.to_dict(with_child_rels=True)

        if with_parent_rels:
            pass

        return d
