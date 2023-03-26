import requests
import json
from datetime import datetime
from time import sleep

glove_id = 1
ccid = 1
ocid = 1

input("Press ENTER to start.")
requests.post('http://127.0.0.1:5000/start', json={'glove_id': glove_id, 'ocid': ocid, 'ccid': ccid})

start_time = datetime.now()

correct = False
# while not correct:
correct = requests.post('http://127.0.0.1:5000/query', json={'primary': {'id': glove_id}, 'label': 'A'}).json()
print(correct)
sleep(2)
requests.post('http://127.0.0.1:5000/stop', json={'glove_id': glove_id})