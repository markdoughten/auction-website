"""Flask configuration variables."""
from os import environ, path
from dotenv import load_dotenv
from urllib.parse import quote

basedir = path.abspath(path.dirname(__file__))
load_dotenv(path.join(basedir, '.env'))


class Config:
    """Set Flask configuration from .env file."""
    
    # General Config
    FLASK_APP="app.py"
    FLASK_ENV = environ.get('FLASK_ENV')

    # Database
    SQLALCHEMY_DATABASE_HOST = environ.get("SQLALCHEMY_DATABASE_HOST")
    SQLALCHEMY_DATABASE_PORT = environ.get("SQLALCHEMY_DATABASE_PORT")
    SQLALCHEMY_DATABASE_USER = environ.get("SQLALCHEMY_DATABASE_USER")
    SQLALCHEMY_DATABASE_PASSWORD = environ.get("SQLALCHEMY_DATABASE_PASSWORD")
    SQLALCHEMY_DATABASE = environ.get("SQLALCHEMY_DATABASE")
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://%s:%s@%s:%s/%s" % (SQLALCHEMY_DATABASE_USER, quote(SQLALCHEMY_DATABASE_PASSWORD), SQLALCHEMY_DATABASE_HOST,SQLALCHEMY_DATABASE_PORT, SQLALCHEMY_DATABASE)
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    #JWT
    SECRET_KEY = environ.get("SECRET_KEY")
    JWT_SECRET_KEY = environ.get("SECRET_KEY")
    JWT_TOKEN_LOCATION = ['headers']
    JWT_VERIFY_SUB = False

    # Test Config
    POPULATE_VALUES = True if environ.get("POPULATE_VALUES") == "True" else False