# Routes
from flask import Blueprint, render_template, request
from ..models.auction import Auctions

search_bp = Blueprint('search_bp', __name__)

@search_bp.route('/search')
def search():
    return render_template('search.html')

@search_bp.route('/results', methods=['POST'])
def results():
    query = request.form.get('query')  # Get the search query from the form
    if query:
        # Search the Auctions model for items matching the query
        results = Auctions.query.filter(Auctions.item_id.ilike(f"%{query}%")).all()
    else:
        results = []

    return render_template('result.html', auctions=results)