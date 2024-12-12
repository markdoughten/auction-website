from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from . import config
from sqlalchemy import text, create_engine
from .utils import constants

db = SQLAlchemy()
jwt = JWTManager()
seed_done=0


def create_db(conf):
    engine = create_engine(conf.SQLALCHEMY_CONN_URI)
    create_str = f"CREATE DATABASE IF NOT EXISTS {conf.SQLALCHEMY_DATABASE};"
    use_str = f"USE {conf.SQLALCHEMY_DATABASE};"

    with engine.connect() as connection:
        try:
            connection.execute(text(create_str))
            connection.execute(text(use_str))
        except Exception as e:
            print("Create DB failed: ",e)
            raise e



def create_app():
    """Construct the core application."""
    app = Flask(__name__, instance_relative_config=False)
    conf = config.Config()
    app.config.from_object(conf)
    CORS(app)
    db.init_app(app)
    jwt.init_app(app)
    create_db(conf)
    with app.app_context():
        from . import routes
        if conf.POPULATE_VALUES:
            from .seeders import seed_all, delete_all_data

        try:
            db.create_all()  # Create sql tables for our data models
        except Exception as e:
            print("Error creating tables: ",e)


        try:
            db.session.execute(text(constants.CREATE_NOTIFS_PROCEDURE))
            db.session.execute(text(constants.CREATE_NOTIFS_TRIGGER))
        except Exception as e:
            print("Error executing raw SQL: ",e)

        return app
