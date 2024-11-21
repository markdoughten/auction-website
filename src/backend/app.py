from flask import Flask, request, redirect, render_template, session, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from datetime import datetime
from os import path, getcwd
from hashlib import sha512

from backend import app
from backend import db

def get_hash(data):
    final_pass = data + "including a random salt";
    return sha512(final_pass.encode('utf-8')).hexdigest()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = password

    def __repr__(self) -> str:
        return '<id %r, Name %r, Email %r, Password %r>' % (self.id, self.username, self.email, self.password)

with app.app_context():
    # exec first time temp data...
    instance_dir = path.abspath(path.join(getcwd(), "..", "instance", "project.db"))
    if not path.isfile(instance_dir):
        db.create_all()

        db.session.add(User('admin', 'admin@example.com', get_hash('mypass')))
        db.session.add(User('guest', 'guest@example.com', get_hash('mypass')))
        db.session.commit()

    users = User.query.all()
    print(users)

@app.route('/')
def index():
    return '<h1>hello world!</h1>'

@app.route('/item/<string:name>')
def item(name):
    return '<h2>hello world! {}</h2>'.format(name)

@app.errorhandler(404)
def page_not_found(e):
    return '<h1>Error page not found...</h1>'

@app.errorhandler(500)
def internal_server_error(e):
    return '<h1>Internal server error...</h1>'

@app.route('/signup', methods=["POST"])
def signup():
    output = {'status': '-1'}
    if request.method == 'POST':
        jsonData = request.json
        email = jsonData.get('email')
        username = jsonData.get('uname')
        password = jsonData.get('password')
        user = User.query.filter((User.email==email) | (User.username==username)).first()
        print(email, username, password, user)
        if email and username and password and (user is None):
            db.session.add(User(username, email, get_hash(password)))
            db.session.commit()
            print("Added succesfully...")
            output['status'] = '0'
        else:
            output['errmsg'] = "some error occurred"

    return output


@app.route('/login', methods=["POST"])
def login():
    output = {'status': '-1'}
    if request.method == 'POST':
        jsonData = request.json
        email = jsonData.get('email')
        password = jsonData.get('password')
        print(email, password)
        if email and password:
            user = User.query.filter((User.email==email) & (User.password==get_hash(password))).first()
            print(user)
            if user:
                output['id'] = str(user.id)
                output['status']= '0'

    return output
