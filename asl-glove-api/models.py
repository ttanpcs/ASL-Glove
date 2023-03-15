from app import db
from sqlalchemy.sql import func
from dataclasses import dataclass
from datetime import datetime

@dataclass
class ClosedCallibrationTrainingSignal(db.Model):
    __tablename__ = 'closed'
    id : int
    voltage_signals : str
    im_signals : str

    id = db.Column(db.Integer, primary_key = True, nullable = False)
    voltage_signals = db.Column(db.String(64), nullable = False)
    im_signals = db.Column(db.String(64), nullable = False)

@dataclass
class OpenCallibrationTrainingSignal(db.Model):
    __tablename__ = 'open'
    id : int
    voltage_signals : str
    im_signals : str

    id = db.Column(db.Integer, primary_key = True, nullable = False)
    voltage_signals = db.Column(db.String(64), nullable = False)
    im_signals = db.Column(db.String(64), nullable = False)

@dataclass
class TrainingSignal(db.Model):
    __tablename__ = 'training'
    id : int
    open_callibration_id : int
    closed_callibration_id : int
    glove_id : int
    time : datetime
    is_start : bool
    label : str
    voltage_signals : str
    im_signals : str

    id = db.Column(db.Integer, primary_key = True, nullable = False)
    open_callibration_id = db.Column(db.Integer, db.ForeignKey('open.id'), nullable = False)
    closed_callibration_id = db.Column(db.Integer, db.ForeignKey('closed.id'), nullable = False)
    glove_id = db.Column(db.Integer, db.ForeignKey('glove.id'), nullable = False)
    time = db.Column(db.DateTime(timezone = True), server_default=func.now(), nullable = False)
    is_start = db.Column(db.Boolean, nullable = False)
    label = db.Column(db.String(16), nullable = False)
    voltage_signals = db.Column(db.String(64), nullable = False)
    im_signals = db.Column(db.String(64), nullable = False)

@dataclass
class Signal(db.Model):     
    __tablename__ = 'signal'
    id : int
    open_callibration_id : int
    closed_callibration_id : int
    glove_id : int
    time : datetime
    is_start : bool
    voltage_signals : str
    im_signals : str

    id = db.Column(db.Integer, primary_key = True, nullable = False)
    open_callibration_id = db.Column(db.Integer, db.ForeignKey('open.id'), nullable = False)
    closed_callibration_id = db.Column(db.Integer, db.ForeignKey('closed.id'), nullable = False)
    glove_id = db.Column(db.Integer, db.ForeignKey('glove.id'), nullable = False)
    time = db.Column(db.DateTime(timezone = True), server_default=func.now(), nullable = False)
    is_start = db.Column(db.Boolean, nullable = False)
    voltage_signals = db.Column(db.String(64), nullable = False)
    im_signals = db.Column(db.String(64), nullable = False)

@dataclass
class Glove(db.Model):
    __tablename__ = 'glove'
    id : int
    is_primary : bool
    port : str

    id = db.Column(db.Integer, primary_key = True, nullable = False)
    is_primary = db.Column(db.Boolean, nullable = False)
    port = db.Column(db.Integer)
    signals = db.relationship('Signal', backref = 'glove', lazy = True)
