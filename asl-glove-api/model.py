import json
from app import db, create_app
from models import Signal, TrainingSignal, ClosedCallibrationTrainingSignal, OpenCallibrationTrainingSignal
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn import metrics
import numpy as np
import pickle
import math
import sys

#DATA SETS PER LETTER
NUM_SETS = 5

# THROW OUT GX

def getCalibration(id, table):
    response = table.query.get(id)
    return (response.voltage_signals, response.im_signals)

def getTrainingFeaturesAndLabels():
    values = TrainingSignal.query.filter(TrainingSignal.is_start==1).all()

    label = []
    feature = []

    print('start label making')

    for v in values:
        label.append(v.label)

    print('finish label making')

    for i in range(len(values) - 1):
        tot_v_values, tot_im_values = normalizeTableValuesWithCalibration(values[i].id, TrainingSignal, values[i+1].id - values[i].id)
        f = np.append(np.array(tot_v_values).flatten(), np.array(tot_im_values).flatten())
        feature.append(f.tolist())

    tot_v_values, tot_im_values = normalizeTableValuesWithCalibration(values[len(values) - 1].id, TrainingSignal)
    f = np.append(np.array(tot_v_values).flatten(), np.array(tot_im_values).flatten())
    feature.append(f.tolist())

    labels = np.array(label)

    features = np.array(feature)

    return features, labels

def normalizeTableValuesWithCalibration(id, table, limit = 0):
    if limit:
        values = table.query.filter(table.id >= id).limit(limit).all()
    else:
        values = table.query.filter(table.id >= id).all()

    # print(values)

    min_values = np.array(list(json.loads('{' + getCalibration(values[0].closed_callibration_id, ClosedCallibrationTrainingSignal)[0] + '}').values()))
    max_values = np.array(list(json.loads('{' + getCalibration(values[0].open_callibration_id, OpenCallibrationTrainingSignal)[0] + '}').values()))

    # print(max_values, min_values)

    if (values[0].glove_id == 1):
        # print('right hand calib')
        min_values = min_values[1:]
        max_values = max_values[1:]
        # print(max_values, min_values)
    else:
        # print('left hand calib')
        min_values = min_values[:-1]
        max_values = max_values[:-1]
        # print(max_values, min_values)

    max_values = np.subtract(max_values, min_values)
    max_values[max_values == 0] = 1

    tot_v_values = []
    tot_im_values = []

    inc = len(values) / NUM_SETS

    i = 0.0

    while i < len(values):
        v = values[math.floor(i)]
        v_values_dict = json.loads('{' + v.voltage_signals + '}')
        im_values_dict = json.loads('{' + v.im_signals + '}')

        # tossing gx
        im_values_dict.pop('gx')
        if v.glove_id == 1:
            # print('right hand')
            v_values_dict.pop('A0')
        else:
            # print('left hand')
            v_values_dict.pop('A7')
        
        v_values = np.array(list(v_values_dict.values()))
        im_values = np.array(list(im_values_dict.values()))

        # normalizing voltage signals

        v_values = np.subtract(v_values, min_values)
        # print(v_values) 

        v_values = np.divide(v_values, max_values)

        # print(v_values) 

        tot_v_values.append(v_values)
        tot_im_values.append(im_values)
        i += inc

    return tot_v_values, tot_im_values

def getLatestPrediction(model, glove_ids , num_rows = 5, num_preds = 1):
    values = Signal.query.filter(Signal.glove_id.in_(glove_ids)).order_by(Signal.time.desc()).limit(num_rows).all() 
    if (len(values) == 0):
        return None   
    id = values[0].id
    for v in values:
        id = v.id
        if v.is_start:
            break

    print(id)

    return getPredictionFromId(id, model, num_preds=num_preds)

def getPredictionFromId(id, model, limit = 0, num_preds = 1):
    tot_v_values, tot_im_values = normalizeTableValuesWithCalibration(id, Signal, limit)
    f = np.append(np.array(tot_v_values).flatten(), np.array(tot_im_values).flatten())
    return getPrediction(f, model, num_preds)

def getPrediction(values, model, num_preds = 1):
    if num_preds == 1:
        prediction = model.predict(values.reshape(1, -1))
        return prediction
    else:
        guesses = model.predict_proba(values.reshape(1, -1))
        predictions = model.classes_[np.argsort(guesses)[:, :-num_preds - 1: -1]]
        return predictions[0]

def loadModel():
    filename = 'trained_model.sav'
    loaded_model = pickle.load(open(filename, 'rb'))
    return loaded_model

def trainModel():
    rf = RandomForestClassifier(n_estimators = 3000, random_state = 42, verbose = 2)

    features, labels = getTrainingFeaturesAndLabels()

    rf.fit(features, labels)

    filename = 'trained_model.sav'
    pickle.dump(rf, open(filename, 'wb'))
    return

# USES 70% OF THE TRAINING TO DATA SET TO TRAIN AND 30% TO TEST ACCURACY
def trainModelWithTestSplit():
    rf = RandomForestClassifier(n_estimators = 3000, criterion='gini', random_state = 42, verbose = 1)

    features, labels = getTrainingFeaturesAndLabels()

    train_features, test_features, train_labels, test_labels = train_test_split(features, labels, test_size = 0.3)

    rf.fit(train_features, train_labels)

    pred_labels = rf.predict(test_features)
    print(pred_labels)
    print(test_labels)

    print("ACCURACY OF THE MODEL: ", metrics.accuracy_score(test_labels, pred_labels))

    filename = 'trained_model.sav'
    pickle.dump(rf, open(filename, 'wb'))
    return

if __name__ == "__main__":
    app = create_app()
    app.app_context().push()

    # print('A' in 'A' 'B' 'C')
    # trainModel()
    model = loadModel()
    # print(getLatestPrediction(model, [1], num_preds= 5))
    # trainModelWithTestSplit()

    label = 'Q'
    text = getLatestPrediction(model, [37], num_preds = 5)
    print(label in text)



