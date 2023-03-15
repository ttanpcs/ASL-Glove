import serial.tools.list_ports
from threading import Thread, Lock
from datetime import datetime
from app import db
from models import Signal, OpenCallibrationTrainingSignal, ClosedCallibrationTrainingSignal, TrainingSignal

class Metadata:
    def __init__(self, ser, ocid, ccid, label) -> None:
        self.ser = ser
        self.ser.baudrate = 9600
        self.ocid = ocid
        self.ccid = ccid
        self.label = label

serial_ports = {}
m = Lock()

def initialize(ocid, ccid, glove_id, label = None):
    if glove_id not in serial_ports.keys():
        ser = serial.Serial()
        serial_ports[glove_id] = Metadata(ser, ocid, ccid, label)            
    else:
        serial_ports[glove_id].ocid = ocid
        serial_ports[glove_id].ccid = ccid
        serial_ports[glove_id].label = label

def start(ocid, ccid, glove_id, port, label = None):
    stop(glove_id)
    m.acquire()
    initialize(ocid, ccid, glove_id, label)
    ser = serial_ports[glove_id].ser
    ser.port = port
    ser.open()
    ser.write(b"1")
    m.release()

def stop(glove_id):
    m.acquire()
    if glove_id in serial_ports.keys():
        ser = serial_ports[glove_id].ser
        if ser.is_open:
            ser.write(b"0")
            ser.close()
    m.release()

def snapshot(glove_id, port, snap_type):
    stop(glove_id)
    m.acquire()
    if snap_type == 'open':
        ocid = -1
        ccid = None
    else:
        ccid = -1
        ocid = None
    initialize(ocid, ccid, glove_id, None)
    ser = serial_ports[glove_id].ser
    ser.port = port
    ser.open()
    ser.write(b"2")
    m.release()

def add_signal(payload, key, value):
    is_start = int(payload[0])
    signals = payload.split("}{")
    im_signals = signals[0][2:]
    voltage_signals = signals[1][:-3] 
    now = datetime.now()

    if value.label is not None:
        db.session.add(
            TrainingSignal(
                open_callibration_id = value.ocid,
                closed_callibration_id = value.ccid,
                glove_id = key,
                time = now,
                is_start = is_start,
                voltage_signals = voltage_signals,
                im_signals = im_signals,
                label = value.label
            )
        )    
    elif value.ocid == -1:
        db.session.add(
            OpenCallibrationTrainingSignal(
                voltage_signals = voltage_signals,
                im_signals = im_signals,
            )
        )
    elif value.ccid == -1:
        db.session.add(
            ClosedCallibrationTrainingSignal(
                voltage_signals = voltage_signals,
                im_signals = im_signals,
            )
        )        
    else:
        db.session.add(
            Signal(
                open_callibration_id = value.ocid,
                closed_callibration_id = value.ccid,
                glove_id = key,
                time = now,
                is_start = is_start,
                voltage_signals = voltage_signals,
                im_signals = im_signals
            )
        )

def update_database(app):
    app.app_context().push()
    while (True):
        m.acquire()
        for key, value in serial_ports.items():
            if value.ser.is_open and value.ser.inWaiting():
                payload = value.ser.readline().decode()
                add_signal(payload, key, value)

        m.release()
        db.session.commit()

def start_database_thread(app):
    database_thread = Thread(target = update_database, args = (app,), daemon = True)
    database_thread.start()
