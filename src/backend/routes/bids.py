@app.route("/auctions/<int:auction_id>/bids", methods=["GET"])
def get_bids(auction_id):
    bids = Bid.query.filter_by(auction_id=auction_id).all()
    return jsonify([{
        "id": bid.id,
        "auction_id": bid.auction_id,
        "users_id": bid.users_id,
        "bid_value": bid.bid_value,
        "bid_active": bid.bid_active
    } for bid in bids])
