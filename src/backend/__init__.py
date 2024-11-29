from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from urllib.parse import quote
from flask_cors import CORS
from flask_jwt_extended import JWTManager

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)
app = Flask(__name__)
jwt = JWTManager(app)
CORS(app)

host="localhost"
user="root"
password="password@123"
database="auction"

app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://%s:%s@%s/%s" % (user, quote(password), host, database)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False  # Optional to suppress warnings
app.config["SECRET_KEY"] = '26c91505-7300-48dc-baa3-ad1d3effe03d'
app.config["JWT_SECRET_KEY"] = "26c91505-7300-48dc-baa3-ad1d3effe03d"
db.init_app(app)

if __name__ == "__main__":
    app.run(debug=True)
