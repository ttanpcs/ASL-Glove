# ASL-Glove

## ASL Glove API and Backend
### Overview
The ASL Glove API is a Flask API that communicates with ASL-Gloves using Serial I/O. 

* asl-glove-api\deploy.py : Used to deploy the 'production.db' database. This deployment will automatically clear the Signal table. Specifying the '--reset' or '-r' parameter will also clear all other tables (Glove, TrainingSignal and the Callibration tables).
* asl-glove-api\routes.py : Used to deploy the flask api.
* asl-glove-api\train.py : Basic python script to fill training database

### Endpoints

* "/register" : POST Endpoint. Payload = {(optional) 'id', 'is_right', 'port'}. This endpoint either registers a new glove in the database or overwrites the properties of an existing glove if 'id' is specified. 'port' corresponds to the COM port in which the glove is communicating through and 'is_right' specifies whether this is a right hand glove or a left hand glove.
* "/snapshot" : POST Endpoint. Payload = {'glove_id', 'type'}. This endpoint is used to take callibration snapshots. 'glove_id' is used to specify which glove the snapshot belongs to and 'type' can either be 'open' or 'closed' where each corresponds to the callibration signal of that type.
* "/start" : POST Endpoint. Payload = {'glove_id', 'ocid', 'ccid', (optional) 'label'}/ This endpoint is used to start recording signals. 'glove_id' is used to specify which glove to record signals from, 'ocid' is used to specify which open callibration signal corresponds to this recording, 'ccid' is used to specify which closed callibration signal corresponds to this recording and 'label' is used to specify what the signal is. If label is not specified, then the signal NOT BE A TRAINING SIGNAL and will be available for querying.
* "/stop" : POST Endpoint. Payload = {'glove_id'}. This endpoint stops recording for the specified glove id.
* "/query" (WIP) : GET Endpoint returns true/false and the last signal / datapoint? processed. Should be called continuously every few milliseconds for accurate results. This should also call the model and do fancy stuff.

### Training
The pipeline for training is as follows (assuming all python dependencies have been installed and both arduinos been uploaded to with test.ino):

1. run `python deploy.py -r` 
2. Modify `train-config.json` to match training aspirations
3. start the flask server by running `python routes.py` in a terminal
4. Start a second terminal instance and run `python train.py` 
5. Follow the instructions in the terminal

### TO DO

- Figure out how best to change deploy.py or train.py so that you don't have to fully reset glove every training iteration? (Maybe modify the JSON config slightly)
- Figure out if data sending should be slowed down for storage concerns
- Figure out /query and possible /signal endpoints (ie interaction with the classifier)