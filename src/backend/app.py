from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from models import db, User, Auction, Bid  # Import models and db from models.py
from datetime import datetime

# Initialize Flask app
app = Flask(__name__, template_folder="src/backend/templates")
CORS(app)

# Configure SQLAlchemy
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:@localhost/auction"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False  # Suppress warnings about deprecated features

# Bind the app to the database
db.init_app(app)

# Routes
@app.route("/")
def index():
    return render_template("index.html")  # Render an HTML file (create index.html in the templates folder)

@app.route("/users", methods=["POST"])
def create_user():
    data = request.json
    new_user = User(
        username=data["username"],
        email=data["email"],
        password=data["password"],
        role=data["role"]
    )
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"message": "User created successfully!"}), 201

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

@app.route("/bids", methods=["POST"])
def place_bid():
    data = request.json
    new_bid = Bid(
        auction_id=data["auction_id"],
        users_id=data["users_id"],
        bid_value=data["bid_value"],
        bid_active=True
    )
    db.session.add(new_bid)
    db.session.commit()
    return jsonify({"message": "Bid placed successfully!"}), 201

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

# Initialize the database
@app.before_request 
def setup():
    db.create_all()

# Run the application
if __name__ == "__main__":
    app.run(debug=True)

