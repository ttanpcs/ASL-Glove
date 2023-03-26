from flask import jsonify, request
from app import create_app, db
from models import Signal, Glove, ClosedCallibrationTrainingSignal, OpenCallibrationTrainingSignal
from model import getLatestPrediction, loadModel
import serial_monitor
import time

app = create_app()
model = loadModel()
serial_monitor.start_database_thread(app)

# @app.route("/signals", methods = ["GET"], strict_slashes = False)
# def signals():
# 	signals = Signal.query.all()

# 	return jsonify(signals)

@app.route("/query", methods = ["POST"], strict_slashes = False)
def query():
	payload = request.get_json()
	if not payload or 'primary' not in payload or 'label' not in payload:
		return "Bad Request", 400
	elif 'secondary' not in payload:
		pred_label = getLatestPrediction(model, [payload['primary']['id']])
		return (payload['label'] == pred_label), 200
	else:
		pred_label = getLatestPrediction(model, [payload['primary']['id'], payload['secondary']['id']])
		return (payload['label'] == pred_label), 200

@app.route("/gloves", methods = ["GET"], strict_slashes = False)
def get_gloves():
	gloves = Glove.query.all()
	return [i['id'] for i in gloves], 200

@app.route("/opencals", methods = ["GET"], strict_slashes = False)
def get_open_callibrations():
	payload = request.get_json()
	if not payload or 'glove_id' not in payload:
		cals = OpenCallibrationTrainingSignal.query.all()
	else:
		cals = OpenCallibrationTrainingSignal.query.filter_by(glove_id = payload['glove_id']).all()
	return [i['id'] for i in cals], 200

@app.route("/closedcals", methods = ["GET"], strict_slashes = False)
def get_closed_callibrations():
	payload = request.get_json()
	if not payload or 'glove_id' not in payload:
		cals = ClosedCallibrationTrainingSignal.query.all()
	else:
		cals = ClosedCallibrationTrainingSignal.query.filter_by(glove_id = payload['glove_id']).all()
	return [i['id'] for i in cals], 200

@app.route("/start", methods = ["POST"], strict_slashes = False)
def start():
	payload = request.get_json()
	if not payload or 'glove_id' not in payload or 'ocid' not in payload or 'ccid' not in payload:
		return "Bad Request", 400
	current_glove = Glove.query.get(payload['glove_id'])
	if current_glove is None:
		return "Bad Request", 400
	if 'label' in payload:
		serial_monitor.start(payload['ocid'], payload['ccid'], payload['glove_id'], current_glove.port, payload['label'])
	else:
		serial_monitor.start(payload['ocid'], payload['ccid'], payload['glove_id'], current_glove.port)

	return "Success", 200

@app.route("/stop", methods = ["POST"], strict_slashes = False)
def stop():
	payload = request.get_json()
	if not payload or 'glove_id' not in payload:
		return "Bad Request", 400
	serial_monitor.stop(payload['glove_id'])

	return "Success", 200

@app.route("/snapshot", methods = ["POST"], strict_slashes = False)
def snapshot():
	payload = request.get_json()
	if not payload or 'glove_id' not in payload or 'type' not in payload:
		return "Bad Request", 400
	current_glove = Glove.query.get(payload['glove_id'])
	if current_glove is None:
		return "Bad Request", 400
	
	if payload['type'] == 'open':
		callibration_type = OpenCallibrationTrainingSignal
	else:
		callibration_type = ClosedCallibrationTrainingSignal
	last_id = callibration_type.query.order_by(callibration_type.id.desc()).first()
	if last_id is not None:
		last_id = last_id.id
	callibration_id = last_id
	
	serial_monitor.snapshot(payload['glove_id'], current_glove.port, payload['type'])
	
	while callibration_id == last_id:
		time.sleep(0.1)
		callibration_id = callibration_type.query.order_by(callibration_type.id.desc()).first()
		if callibration_id is not None:
			callibration_id = callibration_id.id

	return jsonify(id = callibration_id), 200

@app.route("/register", methods = ["POST"], strict_slashes = False)
def register_glove():
	payload = request.get_json()
	if not payload or 'port' not in payload or 'is_primary' not in payload:
		return "Bad Request", 400
	if 'id' in payload:
		current_glove = Glove.query.get(payload['id'])
		if current_glove is not None:
			current_glove.is_primary = payload['is_primary']
			current_glove.port = payload['port']
		else:
			db.session.add(Glove(is_primary = payload['is_primary'], port = payload['port']))

	else:
		db.session.add(Glove(is_primary = payload['is_primary'], port = payload['port']))
	db.session.commit()

	return "Success", 200

if __name__ == "__main__":
	app.run(debug = True)
