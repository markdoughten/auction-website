from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    pass

# Initialize SQLAlchemy
db = SQLAlchemy(model_class=Base)

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(128), unique=True, nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    role = db.Column(db.Enum('Admin', 'Staff', 'User', name='role_enum'), nullable=False)

    def __repr__(self):
        return f"<User {self.id}, Name {self.username}, Email {self.email}, Role {self.role}>"

class Notification(db.Model):
    __tablename__ = 'notification'
    id = db.Column(db.Integer, primary_key=True)
    uid = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.String(255), nullable=True)

    def __repr__(self):
        return f"<Notification {self.id}, UID {self.uid}, Title {self.title}>"

class MetaItemCategory(db.Model):
    __tablename__ = 'meta_item_categories'
    id = db.Column(db.Integer, primary_key=True)
    category_name = db.Column(db.String(255), nullable=False)

    def __repr__(self):
        return f"<MetaItemCategory {self.id}, Name {self.category_name}>"

class MetaItemSubcategory(db.Model):
    __tablename__ = 'meta_item_subcategories'
    id = db.Column(db.Integer, primary_key=True)
    category_id = db.Column(db.Integer, db.ForeignKey('meta_item_categories.id'), nullable=False)
    subcategory_name = db.Column(db.String(255), nullable=False)

    def __repr__(self):
        return f"<MetaItemSubcategory {self.id}, Category {self.category_id}, Name {self.subcategory_name}>"

class MetaItemAttribute(db.Model):
    __tablename__ = 'meta_item_attributes'
    id = db.Column(db.Integer, primary_key=True)
    attribute_name = db.Column(db.String(255), nullable=False)
    subcategory_id = db.Column(db.Integer, db.ForeignKey('meta_item_subcategories.id'), nullable=False)

    def __repr__(self):
        return f"<MetaItemAttribute {self.id}, Subcategory {self.subcategory_id}, Name {self.attribute_name}>"

class Item(db.Model):
    __tablename__ = 'items'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('meta_item_categories.id'), nullable=False)
    subcategory_id = db.Column(db.Integer, db.ForeignKey('meta_item_subcategories.id'), nullable=False)

    def __repr__(self):
        return f"<Item {self.id}, Name {self.name}, Category {self.category_id}, Subcategory {self.subcategory_id}>"

class ItemAttribute(db.Model):
    __tablename__ = 'item_attributes'
    item_id = db.Column(db.Integer, db.ForeignKey('items.id'), primary_key=True)
    attribute_id = db.Column(db.Integer, db.ForeignKey('meta_item_attributes.id'), primary_key=True)
    attribute_value = db.Column(db.String(255), nullable=False)

    def __repr__(self):
        return f"<ItemAttribute Item {self.item_id}, Attribute {self.attribute_id}, Value {self.attribute_value}>"

class Auction(db.Model):
    __tablename__ = 'auctions'
    id = db.Column(db.Integer, primary_key=True)
    item_id = db.Column(db.Integer, db.ForeignKey('items.id'), nullable=False)
    seller_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    initial_price = db.Column(db.Float, nullable=False)
    min_increment = db.Column(db.Float, nullable=False)
    min_price = db.Column(db.Float, nullable=False)
    opening_time = db.Column(db.DateTime, nullable=False)
    closing_time = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.Enum('Open', 'Sold', 'Expired', name='status_enum'), nullable=False)

    def __repr__(self):
        return f"<Auction {self.id}, Item {self.item_id}, Seller {self.seller_id}, Status {self.status}>"

class Bid(db.Model):
    __tablename__ = 'bids'
    id = db.Column(db.Integer, primary_key=True)
    auction_id = db.Column(db.Integer, db.ForeignKey('auctions.id'), nullable=False)
    users_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    bid_value = db.Column(db.Float, nullable=False)
    bid_active = db.Column(db.Boolean, nullable=False)

    def __repr__(self):
        return f"<Bid {self.id}, Auction {self.auction_id}, User {self.users_id}, Value {self.bid_value}>"

class UserQuestion(db.Model):
    __tablename__ = 'user_questions'
    id = db.Column(db.Integer, primary_key=True)
    auction_id = db.Column(db.Integer, db.ForeignKey('auctions.id'), nullable=False)
    asker_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    replier_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    question_text = db.Column(db.String(255), nullable=False)
    is_open = db.Column(db.Boolean, nullable=False)

    def __repr__(self):
        return f"<UserQuestion {self.id}, Auction {self.auction_id}, Asker {self.asker_id}>"

class UserAnswer(db.Model):
    __tablename__ = 'user_answers'
    id = db.Column(db.Integer, primary_key=True)
    question_id = db.Column(db.Integer, db.ForeignKey('user_questions.id'), nullable=False)
    replier_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    reply_text = db.Column(db.String(255), nullable=False)

    def __repr__(self):
        return f"<UserAnswer {self.id}, Question {self.question_id}, Replier {self.replier_id}>"

class Alert(db.Model):
    __tablename__ = 'alerts'
    id = db.Column(db.Integer, primary_key=True)
    item_id = db.Column(db.Integer, db.ForeignKey('items.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    def __repr__(self):
        return f"<Alert {self.id}, Item {self.item_id}, User {self.user_id}>"
