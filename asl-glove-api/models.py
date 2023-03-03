from app import db
from sqlalchemy.sql import func
from dataclasses import dataclass
from datetime import datetime

@dataclass
class Signal(db.Model):     
    id : int
    glove_id : int
    time : datetime
    is_start : bool

    id = db.Column(db.Integer, primary_key = True, nullable = False)
    glove_id = db.Column(db.Integer, db.ForeignKey('glove.id'), nullable = False)
    time = db.Column(db.DateTime(timezone = True), server_default=func.now(), nullable = False)
    is_start = db.Column(db.Boolean, nullable = False)
    # voltage and acceleration signals

@dataclass
class Glove(db.Model):
    id : int
    is_right : bool

    id = db.Column(db.Integer, primary_key = True, nullable = False)
    is_right = db.Column(db.Boolean, nullable = False)
    db.relationship('Signals', backref = 'glove', lazy = True)
    