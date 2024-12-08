from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from . import config

db = SQLAlchemy()
jwt = JWTManager()

def create_app():
    """Construct the core application."""
    app = Flask(__name__, template_folder="templates", instance_relative_config=False)
    conf = config.Config()
    app.config.from_object(conf)
    CORS(app)
    db.init_app(app)
    jwt.init_app(app)

    with app.app_context():

        # Register blueprints for routes
        from .routes.home import home_bp
        from .routes.auth import auth_bp
        from .routes.search import search_bp
        from .routes.notifications import notifications_bp
        from .routes.auctions import auctions_bp
        app.register_blueprint(home_bp)
        app.register_blueprint(auth_bp)
        app.register_blueprint(search_bp)
        app.register_blueprint(notifications_bp)
        app.register_blueprint(auctions_bp)

        # Create database tables
        try:
            db.create_all()  # Create SQL tables for our data models
            print("Database tables created successfully.")
        except Exception as e:
            print("Error creating tables:", e)

        # Populate database with dummy data if enabled in configuration
        if conf.POPULATE_VALUES:
            try:
                from .utils.data import populate_data
                populate_data()
                print("Dummy data populated successfully.")
            except Exception as e:
                print("Error populating dummy data:", e)

        return app