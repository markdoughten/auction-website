from flask import Flask, request, redirect, render_template, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from flask_cors import CORS

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)
app = Flask(__name__)
CORS(app)

app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:password@localhost/auction"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False  # Optional to suppress warnings
db.init_app(app)

if __name__ == "__main__":
    app.run(debug=True)
