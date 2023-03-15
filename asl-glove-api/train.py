import requests
import os 
import json

def filter_zeros(pair):
    key, value = pair
    if not value:
        return False
    return True 

def send_stop_requests(gloves):
    for glove in gloves:
        requests.post('http://127.0.0.1:5000/stop', json={'glove_id': glove['id']})

def send_start_requests(gloves, label):
    for glove in gloves:
        requests.post('http://127.0.0.1:5000/start', json={'glove_id': glove['id'], 'ocid': glove['ocid'], 'ccid': glove['ccid'], 'label': label})

with open('train-config.json') as f:
    config = json.load(f)
    for glove in config['gloves']:
        print(f'Now processing glove: {glove["id"]}')
        glove_request = requests.post('http://127.0.0.1:5000/register', json={'id': glove['id'],  'is_primary': glove['is_primary'], 'port': glove['port']})
        if glove_request.status_code == 400:
            print('Glove Request Failed')
            exit
        
        input("Press ENTER to take open callibration snapshot.")
        o_request = requests.post('http://127.0.0.1:5000/snapshot', json={'glove_id': glove['id'],  'type': 'open'})
        glove['ocid'] = o_request.json()['id']
        if o_request.status_code == 400:
            print('Open Callibration Request Failed')
            exit
        
        input("Press ENTER to take closed callibration snapshot.")
        c_request = requests.post('http://127.0.0.1:5000/snapshot', json={'glove_id': glove['id'], 'type': 'closed'})
        glove['ccid'] = c_request.json()['id']
        if c_request.status_code == 400:
            print('Closed Callibration Request Failed')
            exit
        os.system('cls')

    non_zero_labels = dict(filter(filter_zeros, config['labels'].items()))
    total = sum(non_zero_labels.values())
    for key, value in non_zero_labels.items():
        for i in range(value, 0, -1):
            print(f'There are {total} total unfilled labels and {i} unfilled labels for {key}.')
            input(f'Press ENTER to start recording for {key}.')
            send_start_requests(config['gloves'], key)
            total -= 1
            input(f'Press ENTER to stop recording for {key}.')
            send_stop_requests(config['gloves'])
            os.system('cls')
