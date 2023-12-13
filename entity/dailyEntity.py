from flask_sqlalchemy import SQLAlchemy
from config.dbconfig import db
from datetime import date, time


class Daily(db.Model):
    __tablename__ = 'daily'

    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    factor_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    date = db.Column(db.Date)
    alcohol = db.Column(db.Boolean)
    exercise = db.Column(db.Boolean)
    stress = db.Column(db.Boolean)
    snoring = db.Column(db.Integer)
    non_snoring = db.Column(db.Integer)
    intensity = db.Column(db.Integer)
    sleep_time = db.Column(db.Integer)