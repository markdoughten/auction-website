from .. import db

"""
Add auction and bid here?
"""

class Auctions(db.Model):
    __tablename__ = 'auctions'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    item_id = db.Column(db.Integer, nullable=False)
    seller_id = db.Column(db.Integer, nullable=False)
    initial_price = db.Column(db.Float, nullable=False)
    min_increment = db.Column(db.Float, nullable=False)
    min_price = db.Column(db.Float, nullable=False)
    opening_time = db.Column(db.DateTime, nullable=False)
    closing_time = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.Enum('Open', 'Sold', 'Expired', name='status_enum'), nullable=False)

    def __repr__(self):
        return f"<Auction {self.id}, Item {self.item_id}, Seller {self.seller_id}, Status {self.status}>"

class Bids(db.Model):
    __tablename__ = 'bids'
    id = db.Column(db.Integer, primary_key=True)
    auction_id = db.Column(db.Integer, nullable=False)
    users_id = db.Column(db.Integer, nullable=False)
    bid_value = db.Column(db.Float, nullable=False)
    bid_active = db.Column(db.Float, nullable=False)