@app.route("/auctions", methods=["POST"])
def create_auction():
    data = request.json
    new_auction = Auction(
        item_id=data["item_id"],
        seller_id=data["seller_id"],
        initial_price=data["initial_price"],
        min_increment=data["min_increment"],
        min_price=data["min_price"],
        opening_time=datetime.fromisoformat(data["opening_time"]),
        closing_time=datetime.fromisoformat(data["closing_time"]),
        status="Open"
    )
    db.session.add(new_auction)
    db.session.commit()
    return jsonify({"message": "Auction created successfully!"}), 201

@app.route("/auctions/<int:auction_id>", methods=["POST"])
def render_auction():
    # query for auction data based on id
    return render_template("auction.html")  # Render an HTML file (create index.html in the templates folder)