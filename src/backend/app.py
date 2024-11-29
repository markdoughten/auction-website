from backend import app, db, jwt
from flask_jwt_extended import jwt_required

from backend.src import users, login

class Auction(db.Model):
    __tablename__ = 'auctions'
    id = db.Column(db.Integer, primary_key=True)
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


@app.route('/')
@jwt_required()
def index():
    with db.session() as session:
        auctions = session.query(Auction).all()

    html_content = '<h1>Auctions</h1><table border="1">'
    html_content += '<tr><th>ID</th><th>Item Name</th><th>Starting Bid</th><th>Status</th></tr>'
    for auction in auctions:
        html_content += f'<tr><td>{auction.id}</td><td>{auction.item_name}</td><td>{auction.starting_bid}</td><td>{auction.status}</td></tr>'
    html_content += '</table>'
    return html_content

@app.errorhandler(404)
def page_not_found(e):
    return '<h1>Error page not found...</h1>'


@app.errorhandler(500)
def internal_server_error(e):
    return '<h1>Internal server error...</h1>'
