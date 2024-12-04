from backend import app, db, jwt
from flask_jwt_extended import jwt_required
from backend.src import login, dashboard, admin

@app.errorhandler(404)
def page_not_found(e):
    return '<h1>Error page not found...</h1>'


@app.errorhandler(500)
def internal_server_error(e):
    return '<h1>Internal server error...</h1>'
