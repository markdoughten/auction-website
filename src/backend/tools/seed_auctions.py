from ..models.auction import Auctions
from ..db_ops.common import db_create_one
from datetime import datetime

def generate_auction(itemid, sellerId):
    return Auctions(
        item_id = itemid,
        seller_id = sellerId,
        initial_price = 1000 + sellerId,
        min_price = 1300 + itemid,
        min_increment = 10,
        closing_time = datetime.strptime("1/" + str(itemid) +"/2025 9:49:05", '%m/%d/%Y %H:%M:%S'),
        status="Open"
    )


def seed_auctions():
    for i in range(1,7):
        auction = generate_auction(i, 7-i)
        db_create_one(auction)
