from ..utils import constants
from ..models.auction import Auctions
from flask import request, jsonify
from flask import current_app as app
from flask_jwt_extended import jwt_required
from flask import Blueprint, render_template
from datetime import datetime
from flask import request, jsonify, redirect, url_for, flash
from flask_jwt_extended import jwt_required, get_jwt_identity

auctions_bp = Blueprint('auctions_bp', __name__)

@auctions_bp.route("/auction", methods=["GET", "POST"])
@jwt_required()
def auction():
    if request.method == "GET":
        # Render the auction creation form
        return render_template("post.html")

    if request.method == "POST":
        # Extract data from the form
        item_name = request.form.get("item_name")
        initial_price = request.form.get("initial_price", type=float)
        min_increment = request.form.get("min_increment", type=float)
        min_price = request.form.get("min_price", type=float)
        opening_time = request.form.get("opening_time")
        closing_time = request.form.get("closing_time")

        # Validate the input
        if not item_name or not initial_price or not min_increment or not min_price or not opening_time or not closing_time:
            flash("All fields are required.", "error")
            return redirect(url_for("auctions_bp.create_auction"))

        # Create a new auction object
        seller_id = get_jwt_identity()  # Get the logged-in user ID
        new_auction = Auctions(
            item_name=item_name,
            seller_id=seller_id,
            initial_price=initial_price,
            min_increment=min_increment,
            min_price=min_price,
            opening_time=datetime.fromisoformat(opening_time),
            closing_time=datetime.fromisoformat(closing_time),
            status="Open"
        )

        # Save the auction to the database
        db.session.add(new_auction)
        db.session.commit()

        flash("Auction created successfully!", "success")
        return redirect(url_for("home_bp.home"))

@auctions_bp.route("/auctions/<int:auction_id>", methods=["POST"])
def render_auction():
    # query for auction data based on id
    return render_template("auction.html")  # Render an HTML file (create index.html in the templates folder)

@auctions_bp.route('/get_items', methods=["POST"])
@jwt_required()
def get_items():
    output = {}
    if request.method == 'POST':
        Auctions.query.filter()
        return jsonify(output)

    output[constants.STATUS] = constants.STATUS_RESPONSE.FAILURE.value
    output[constants.MESSAGE] = constants.FAILURE_MSG
    return jsonify(output)

@auctions_bp.route('/add_items', methods=["POST"])
def add_items():
    print("Entered add_items")
    failed = []
    dir_path = os.path.dirname(os.path.realpath(__file__))
    with open(os.path.join(dir_path, 'dict/meta_items.json')) as f:
        m_itm = json.load(f)
        for item in m_itm:
            categs = m_itm[item]
            for categ in categs:
                attrs = categs[categ]
                for attr in attrs:
                    sub_item, retval = item_meta.add_item_attr(item, categ, attr)
                    if sub_item is None:
                        failed.append((item, categ, attr))
                        print(failed[-1], "add failed")
                    elif not retval:
                        failed.append((item, categ, attr))
                        print(failed[-1], "item already added")

    response = {}
    response[constants.STATUS] = len(failed)
    response[constants.MESSAGE] = failed if len(failed) else "items added successfully"
    return response