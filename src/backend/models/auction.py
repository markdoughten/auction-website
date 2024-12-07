from dataclasses import dataclass
from .. import db

"""
Add auction and bid here?
"""

@dataclass
class Auctions(db.Model):
    __tablename__ = 'auctions'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    item_id = db.Column(db.Integer, db.ForeignKey("items.id"), nullable=False)
    seller_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    initial_price = db.Column(db.Float, nullable=False)
    min_increment = db.Column(db.Float, nullable=False)
    min_price = db.Column(db.Float, nullable=False)
    opening_time = db.Column(db.DateTime, nullable=False)
    closing_time = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.Enum('Open', 'Sold', 'Expired', name='status_enum'), nullable=False)

    a_user = db.relationship("User", foreign_keys=[seller_id], back_populates="a_user")
    a_item = db.relationship("Item", foreign_keys=[item_id], back_populates="a_item")
    b_item = db.relationship("Bids", back_populates="b_item")
    def __repr__(self):
        return f"<Auction {self.id}, Item {self.item_id}, Seller {self.seller_id}, Status {self.status}>"

@dataclass
class Bids(db.Model):
    __tablename__ = 'bids'
    id = db.Column(db.Integer, primary_key=True)
    auction_id = db.Column(db.Integer, db.ForeignKey("auctions.id"), nullable=False)
    users_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    bid_value = db.Column(db.Float, nullable=False)
    bid_active = db.Column(db.Float, nullable=False)

    b_user = db.relationship("User", foreign_keys=[users_id], back_populates="b_user")
    b_item = db.relationship("Auctions", foreign_keys=[auction_id], back_populates="b_item")
