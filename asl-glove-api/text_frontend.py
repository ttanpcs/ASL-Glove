import requests
import json
from datetime import datetime
from time import sleep
import random

glove_id = 1
ccid = 1
ocid = 1

input("Press ENTER to take open callibration snapshot.")
o_request = requests.post('http://127.0.0.1:5000/snapshot', json={'glove_id': glove_id,  'type': 'open'})
ocid = o_request.json()['id']
if o_request.status_code == 400:
    print('Open Callibration Request Failed')
    exit

input("Press ENTER to take closed callibration snapshot.")
c_request = requests.post('http://127.0.0.1:5000/snapshot', json={'glove_id': glove_id, 'type': 'closed'})
ccid = c_request.json()['id']
if c_request.status_code == 400:
    print('Closed Callibration Request Failed')
    exit

input("Press ENTER to start.")
requests.post('http://127.0.0.1:5000/start', json={'glove_id': glove_id, 'ocid': ocid, 'ccid': ccid})

start_time = datetime.now()
with open('supported_signs.json') as f:
    supported_signs = json.load(f)
    current_sign = random.choice(supported_signs['one_hand_signs'])
    correct = False
    while not correct:
        correct = requests.post('http://127.0.0.1:5000/query', json={'primary': {'id': glove_id}, 'label': current_sign}).json()
        sleep(0.1)
    requests.post('http://127.0.0.1:5000/stop', json={'glove_id': glove_id})