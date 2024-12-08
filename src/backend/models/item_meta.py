from sqlalchemy.orm import relationship
from sqlalchemy import ForeignKey, UniqueConstraint
from dataclasses import dataclass
from .. import db
from sqlalchemy.orm import Mapped
from typing import List

class MetaItemCategory(db.Model):
    __tablename__ = 'meta_item_categories'
    id:int = db.Column(db.Integer, primary_key=True, autoincrement=True)
    category_name:str = db.Column(db.String(128), nullable=False, unique=True)

    #Relationships
    subcategories:Mapped[List["MetaItemSubCategory"]] = relationship(back_populates="category",cascade="all, delete")

    # methods
    def to_dict(self, with_child_rels=False, with_parent_rels=False):
        d = {}
        d["id"] = self.id
        d["categoryName"] = self.category_name

        if (with_child_rels):
            d["subcategories"] = list(map(lambda x:x.to_dict(with_child_rels=True),self.subcategories))

        if (with_parent_rels):
            pass

        return d



class MetaItemSubCategory(db.Model):
    __tablename__ = 'meta_item_subcategories'
    id:int = db.Column(db.Integer, primary_key=True, autoincrement=True)
    category_id:int = db.Column(db.Integer, ForeignKey("meta_item_categories.id",ondelete="CASCADE"), nullable=False)
    subcategory_name:str = db.Column(db.String(128), nullable=False)
    __table_args__ = (UniqueConstraint('category_id', 'subcategory_name', name='_cat_subcat_uc'),)
    
    #Relationships
    category:Mapped[MetaItemCategory] = relationship(back_populates="subcategories")
    attributes:Mapped[List["MetaItemAttribute"]] = relationship(back_populates="subcategory",cascade="all, delete")

    #methods
    def to_dict(self, with_child_rels=False, with_parent_rels=False):
        d={}
        d["id"] = self.id
        d["categoryId"] = self.category_id
        d["subcategoryName"] = self.subcategory_name

        if (with_child_rels):
            d["attributes"] = list(map(lambda x:x.to_dict(with_child_rels=True),self.attributes))

        if (with_parent_rels):
            d["category"] = self.category.to_dict(with_parent_rels=True)

        return d


class MetaItemAttribute(db.Model):
    __tablename__ = 'meta_item_attributes'
    id:int = db.Column(db.Integer, primary_key=True, autoincrement=True)
    attribute_name:str = db.Column(db.String(128), nullable=False)
    subcategory_id:int = db.Column(db.Integer, ForeignKey("meta_item_subcategories.id", ondelete="CASCADE"), nullable=False)
    __table_args__ = (UniqueConstraint('subcategory_id', 'attribute_name', name='_subcat_attr_uc'),)

    #Relationships
    subcategory:Mapped[MetaItemSubCategory] = relationship(back_populates="attributes")

def create_new_item(item_name):
    item = MetaItemCategory.query.filter(MetaItemCategory.category_name==item_name).first()
    if item is None:
        item = MetaItemCategory()
        item.category_name = item_name
        db.session.add(item)
        db.session.commit()
        return (item, True)

    return (item, False)

def add_item_categ(item_name, categ_name):
    item, retval = create_new_item(item_name)
    if item is None:
        return (None, False)

    sub_item = MetaItemSubCategory.query.filter((MetaItemSubCategory.category_id==item.id) & (MetaItemSubCategory.subcategory_name==categ_name)).first()
    if sub_item is None:
        sub_item = MetaItemSubCategory()
        sub_item.category_id = item.id
        sub_item.subcategory_name = categ_name
        db.session.add(sub_item)
        db.session.commit()
        return (sub_item, True)

    return (sub_item, False)

def add_item_attr(item_name, categ_name, attr_name):
    sub_item, retval = add_item_categ(item_name, categ_name)
    if sub_item is None:
        return (None, False)

    item_attr = MetaItemAttribute.query.filter((MetaItemAttribute.subcategory_id==sub_item.id) & (MetaItemAttribute.attribute_name==attr_name)).first()
    if item_attr is None:
        item_attr = MetaItemAttribute()
        item_attr.subcategory_id = sub_item.id
        item_attr.attribute_name = attr_name
        db.session.add(item_attr)
        db.session.commit()
        return (item_attr, True)

    return (item_attr, False)

    #methods
    def to_dict(self,with_child_rels=False, with_parent_rels=False):
        d={}
        d["id"] = self.id
        d["attributeName"] = self.attribute_name
        d["subcategoryId"] = self.subcategory_id

        if (with_child_rels):
            pass
        
        if (with_parent_rels):
            d["subcategory"] = self.subcategory.to_dict(with_parent_rels=True)
        
        return d
