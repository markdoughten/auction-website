from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from . import config

db = SQLAlchemy()
jwt = JWTManager()

def create_app():
    
    """Construct the core application."""
    app = Flask(__name__, instance_relative_config=False)
    conf = config.Config()
    app.config.from_object(conf)
    CORS(app)
    db.init_app(app)
    jwt.init_app(app)

    with app.app_context():
        from . import routes
        if conf.POPULATE_VALUES:
            from . import tools

        try:
            db.create_all()  # Create sql tables for our data models
        except Exception as e:
            print("Error creating tables: ",e)
        return app
