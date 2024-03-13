#!/usr/bin/env python3
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)

    #app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////home/tnlnews/db/tnlnews.db'
    # Local development
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tnlnews.db'
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config['SECRET_KEY'] = 'thisisadummyvaluereplaceitwithsomethinglikeanenvvar!'
    app.config['SESSION_COOKIE_SECURE'] = True
    app.config['REMEMBER_COOKIE_SECURE'] = True

    db.init_app(app)

    with app.app_context():
        from . import routes
        db.create_all()
        return app
