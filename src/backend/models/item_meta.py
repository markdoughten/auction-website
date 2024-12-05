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
    attribute_name:str = db.Column(db.String(128), nullable=False)
    subcategory_id:int = db.Column(db.Integer, ForeignKey("meta_item_subcategories.id"))

    #Relationships
    subcategory = relationship("MetaItemSubCategory")
