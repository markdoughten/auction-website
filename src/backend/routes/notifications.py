from flask import Blueprint, render_template, request, jsonify, session, redirect, url_for, flash
from flask_jwt_extended import (jwt_required, get_jwt_identity)
from datetime import datetime
from ..models.notification import Notification, Alert
from ..models.auction import Auctions
from ..utils import constants

notifications_bp = Blueprint('notifications_bp', __name__)

@notifications_bp.route('/auction/<int:item_id>/action', methods=["POST"])
@jwt_required()
def bid_or_notify(item_id):
    action = request.form.get('action')
    user_id = get_jwt_identity()  # Get the logged-in user's ID

    if action == 'notify':
        # Check if the user is already signed up for notifications
        alert = Alert.query.filter_by(item_id=item_id, user_id=user_id).first()
        if alert:
            flash("You are already signed up for notifications on this item.", "info")
        else:
            # Create a new alert
            new_alert = Alert(item_id=item_id, user_id=user_id)
            db.session.add(new_alert)
            db.session.commit()
            flash("You have successfully signed up for notifications!", "success")

    elif action == 'bid':
        bid_amount = request.form.get('bid_amount', type=float)
        if bid_amount:
            # Retrieve the auction and place a bid
            auction = Auctions.query.filter_by(id=item_id).first()
            if not auction:
                flash("Auction not found!", "error")
                return redirect(url_for('home_bp.home'))

            # Add logic to handle bidding
            if bid_amount >= auction.min_price:
                # Assume `Auction.place_bid()` handles bid placement
                auction.place_bid(user_id=user_id, bid_amount=bid_amount)
                db.session.commit()
                flash("Your bid has been placed successfully!", "success")
            else:
                flash("Bid amount must be greater than or equal to the minimum price!", "error")
        else:
            flash("Invalid bid amount!", "error")

    return redirect(url_for('home_bp.home'))

@notifications_bp.route('/auction/<int:item_id>/notify', methods=["POST"])
@jwt_required()
def notify_user(item_id):
    user_id = get_jwt_identity()  # Get the logged-in user's ID

    # Check if the user is already signed up for notifications
    alert = Alert.query.filter_by(item_id=item_id, user_id=user_id).first()
    if alert:
        flash("You are already signed up for notifications on this item.", "info")
    else:
        # Create a new alert
        new_alert = Alert(item_id=item_id, user_id=user_id)
        db.session.add(new_alert)
        db.session.commit()
        flash("You have successfully signed up for notifications!", "success")

    return redirect(url_for('home_bp.home'))
