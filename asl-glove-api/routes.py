from flask import jsonify, request
from app import create_app, db
from models import Signal, Glove

app = create_app()

# Define a route to fetch the avaialable articles

@app.route("/signals", methods = ["GET"], strict_slashes = False)
def signals():
	signals = Signal.query.all()

	return jsonify(signals)

@app.route("/gloves", methods = ["GET"], strict_slashes = False)
def gloves(glove_id):
	current_glove = Glove.query.get_or_404(glove_id)

	return jsonify(current_glove)

@app.route("/register", methods = ["POST"], strict_slashes = False)
def register_glove():
	ir = request.form['is_right']
	
	db.session.add(Glove(is_right = ir))
	db.session.commit()

	return None # Might want to redirect the url to something else


# Used to send signals
# @app.route("/record", methods = ["POST"], strict_slashes = False)
# def send_recording():

if __name__ == "__main__":
	app.run(debug = True)
