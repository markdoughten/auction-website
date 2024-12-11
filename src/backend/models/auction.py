from .. import db
from ..models.item import Item
from ..models.user import User
from sqlalchemy.orm import relationship, Mapped
from sqlalchemy import ForeignKey
from sqlalchemy.sql import func

"""
Add auction and bid here?
"""

class Auctions(db.Model):
    __tablename__ = 'auctions'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    item_id = db.Column(db.Integer, ForeignKey("items.id", ondelete="CASCADE"), nullable=False)
    seller_id = db.Column(db.Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    initial_price = db.Column(db.Float, nullable=False)
    min_increment = db.Column(db.Float, nullable=False)
    min_price = db.Column(db.Float, nullable=False)
    opening_time = db.Column(db.DateTime, nullable=False, server_default=func.now())
    closing_time = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.Enum('Open', 'Sold', 'Expired', name='status_enum'), nullable=False)

    #Relationships
    item:Mapped[Item] = relationship()
    seller:Mapped[User] = relationship()

    #methods
    def __repr__(self):
        return f"<Auction {self.id}, Item {self.item_id}, Seller {self.seller_id}, Status {self.status}>"

    def to_dict(self, with_child_rels=False, with_parent_rels=False):
        d={}
        d["id"] = self.id
        d["itemId"] = self.item_id
        d["sellerId"] = self.seller_id
        d["initialPrice"] = self.initial_price
        d["minIncrement"] = self.min_increment
        d["minPrice"] = self.min_price
        d["openingTime"] = self.opening_time
        d["closingTime"] = self.closing_time

        if with_child_rels:
            pass

        if with_parent_rels:
            d["item"] = self.item.to_dict(with_child_rels=True)
            d["seller"] = self.seller.to_dict()

        return d


class Bids(db.Model):
    __tablename__ = 'bids'
    id = db.Column(db.Integer, primary_key=True)
    auction_id = db.Column(db.Integer, ForeignKey("auctions.id", ondelete="CASCADE"), nullable=False)
    bidder_id = db.Column(db.Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    bid_value = db.Column(db.Float, nullable=False)
    bid_active = db.Column(db.Boolean, nullable=False)

    #Relationships
    bidder:Mapped[User] = relationship()
    auction:Mapped[Auctions] = relationship()

    #methods
    def to_dict(self, with_child_rels=False, with_parent_rels=False):
        d={}
        d["id"] = self.id
        d["auctionId"] = self.auction_id
        d["bidderId"] = self.bidder_id
        d["bidValue"] = self.bid_value
        d["bidActive"] = self.bid_active

        if with_child_rels:
            pass
        
        if with_parent_rels:
            d["bidder"] = self.bidder.to_dict()
            d["auction"] = self.auction.to_dict(with_parent_rels=True)
        
        return d
