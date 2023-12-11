from flask_sqlalchemy import SQLAlchemy
from config.dbconfig import db



class User(db.Model):
    __tablename__ = 'users'

    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)
    gender = db.Column(db.String(10))
    birthday = db.Column(db.Date)
    firstname = db.Column(db.String(50))
    lastname = db.Column(db.String(50))
    weight = db.Column(db.Float(precision=5))
    height = db.Column(db.Float(precision=5))
    medical_condition = db.Column(db.String(255))
    nationality = db.Column(db.String(50))


    