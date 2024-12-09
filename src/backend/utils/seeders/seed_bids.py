from ...models.auction import Bids
from ...db_ops.common import db_create_one


def gen_bid(userid, auctionid, value):
    return Bids(
        auction_id = auctionid,
        bidder_id = userid,
        bid_value = value,
        bid_active = True
    )


def seed_bids():
    for i in range(1,7):
        for j in range(4):
            bid = gen_bid(20+(4*i)+j, i, 1000+i*j)
            db_create_one(bid)
