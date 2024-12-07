from sqlalchemy.orm import relationship
from sqlalchemy import ForeignKey
from dataclasses import dataclass
from .. import db

@dataclass
class MetaItemCategory(db.Model):
    __tablename__ = 'meta_item_categories'
    id:int = db.Column(db.Integer, primary_key=True, autoincrement=True)
    category_name:str = db.Column(db.String(128), nullable=False, unique=True)

@dataclass
class MetaItemSubCategory(db.Model):
    __tablename__ = 'meta_item_subcategories'
    id:int = db.Column(db.Integer, primary_key=True, autoincrement=True)
    category_id:int = db.Column(db.Integer, ForeignKey("meta_item_categories.id"))
    subcategory_name:str = db.Column(db.String(128), nullable=False)

    #Relationships
    category = relationship("MetaItemCategory")

@dataclass
class MetaItemAttribute(db.Model):
    __tablename__ = 'meta_item_attributes'
    id:int = db.Column(db.Integer, primary_key=True, autoincrement=True)
    subcategory_id:int = db.Column(db.Integer, ForeignKey("meta_item_subcategories.id"))
    attribute_name:str = db.Column(db.String(128), nullable=False)

    #Relationships
    subcategory = relationship("MetaItemSubCategory")

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
