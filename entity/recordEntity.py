from flask_sqlalchemy import SQLAlchemy
from config.dbconfig import db
from datetime import date, time



class Record(db.Model):
    __tablename__ = 'record'

    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    record_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    date = db.Column(db.Date)
    time_start = db.Column(db.Time)
    time_stop = db.Column(db.Time)
    path = db.Column(db.String(255))
    model_result = db.Column(db.Text)
    calls = db.Column(db.Integer)