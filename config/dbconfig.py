from flask_sqlalchemy import SQLAlchemy
import pymysql

DATABASE_URI = 'mysql+pymysql://jiji:grumpyissad@snorewise-db.c4d8pauabtno.us-east-1.rds.amazonaws.com/snorewise-db'

db = SQLAlchemy()

def init_app(app):
    app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URI
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
