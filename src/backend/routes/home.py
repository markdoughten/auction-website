# Routes
from flask import Blueprint, render_template
from ..models.auction import Auctions

home_bp = Blueprint('home_bp', __name__)

@home_bp.route('/')
def home():
    auctions = Auctions.query.filter(Auctions.status == 'Open').all()
    return render_template('home.html', auctions=auctions)