import json
import sqlite3
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn import metrics
import numpy as np
import pickle
import math

#DATA SETS PER LETTER
NUM_SETS = 5

conn = sqlite3.connect('production.db')
c = conn.cursor()

# THROW OUT GX

def getClosedCalibration(id):
    c.execute('SELECT voltage_signals,im_signals FROM closed WHERE id=?', [id])
    return c.fetchone()

def getOpenCalibration(id):
    c.execute('SELECT voltage_signals,im_signals FROM open WHERE id=?', [id])
    return c.fetchone()

def getTrainingFeaturesAndLabels():
    c.execute('SELECT * FROM training WHERE is_start')
    values = c.fetchall()

    label = []
    feature = []

    print('start label making')

    for v in values:
        label.append(v[6])

    print('finish label making')

    for i in range(len(values) - 1):
        tot_v_values, tot_im_values = getSingleTrainingValueWithCalibration(values[i][0], values[i+1][0] - values[i][0])
        f = np.append(np.array(tot_v_values).flatten(), np.array(tot_im_values).flatten())
        feature.append(f.tolist())

    tot_v_values, tot_im_values = getSingleTrainingValueWithCalibration(values[len(values) - 1][0])
    f = np.append(np.array(tot_v_values).flatten(), np.array(tot_im_values).flatten())
    feature.append(f.tolist())

    labels = np.array(label)

    features = np.array(feature)

    return features, labels

def getSingleTrainingValueWithCalibration(id, limit=0):
    if limit:
        c.execute('SELECT * FROM training WHERE id>=? LIMIT ?', [id, limit])
    else:
        c.execute('SELECT * FROM training WHERE id>=?', [id])

    values = c.fetchall()

    min_values = np.array(list(json.loads('{' + getClosedCalibration(values[0][2])[0] + '}').values()))
    max_values = np.array(list(json.loads('{' + getOpenCalibration(values[0][1])[0] + '}').values()))

    print(max_values, min_values)

    if (values[0][3] == 1):
        print('right hand calib')
        min_values = min_values[1:]
        max_values = max_values[1:]
        print(max_values, min_values)
    else:
        print('left hand calib')
        min_values = min_values[:-1]
        max_values = max_values[:-1]
        print(max_values, min_values)

    max_values = np.subtract(max_values, min_values)

    tot_v_values = []
    tot_im_values = []

    inc = len(values) / NUM_SETS

    i = 0.0

    while i < len(values):
        v = values[math.floor(i)]
        v_values_dict = json.loads('{' + v[7] + '}')
        im_values_dict = json.loads('{' + v[8] + '}')

        # tossing gx and extra voltage reading
        im_values_dict.pop('gx')
        if v[3] == 1:
            print('right hand')
            v_values_dict.pop('A0')
        else:
            print('left hand')
            v_values_dict.pop('A7')
        
        v_values = np.array(list(v_values_dict.values()))
        im_values = np.array(list(im_values_dict.values()))

        # normalizing voltage signals

        v_values = np.subtract(v_values, min_values)

        v_values = np.divide(v_values, max_values)

        tot_v_values.append(v_values)
        tot_im_values.append(im_values)
        i += inc

    return tot_v_values, tot_im_values

def normalizeSignalValuesWithCalibration(id, limit = 0):
    if limit:
        c.execute('SELECT * FROM signal WHERE id>=? LIMIT ?', [id, limit])
    else:
        c.execute('SELECT * FROM signal WHERE id>=?', [id])

    values = c.fetchall()

    # print(values)

    min_values = np.array(list(json.loads('{' + getClosedCalibration(values[0][2])[0] + '}').values()))
    max_values = np.array(list(json.loads('{' + getOpenCalibration(values[0][1])[0] + '}').values()))

    # print(max_values, min_values)

    if (values[0][3] == 1):
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

    tot_v_values = []
    tot_im_values = []

    inc = len(values) / NUM_SETS

    i = 0.0

    while i < len(values):
        v = values[math.floor(i)]
        v_values_dict = json.loads('{' + v[6] + '}')
        im_values_dict = json.loads('{' + v[7] + '}')

        # tossing gx
        im_values_dict.pop('gx')
        if v[3] == 1:
            # print('right hand')
            v_values_dict.pop('A0')
        else:
            # print('left hand')
            v_values_dict.pop('A7')
        
        v_values = np.array(list(v_values_dict.values()))
        im_values = np.array(list(im_values_dict.values()))

        # normalizing voltage signals

        v_values = np.subtract(v_values, min_values)

        v_values = np.divide(v_values, max_values)

        tot_v_values.append(v_values)
        tot_im_values.append(im_values)
        i += inc

    return tot_v_values, tot_im_values

def getLatestPrediction(model, glove_ids , num_rows = 20):
    glove_id_str = []
    for id in glove_ids:
        glove_id_str.append(str(id))
    glove_id_sql = ",".join(glove_id_str)
    print(glove_id_sql)
    c.execute('SELECT id,is_start FROM signal WHERE glove_id IN (?) ORDER BY time DESC LIMIT ? ', [glove_id_sql, num_rows])
    values = c.fetchall()
    
    id = values[0][0]

    for v in values:
        id = v[0]
        if v[1]:
            break
    print(id)

    return getPredictionFromId(id, model)

def getPredictionFromId(id, model, limit = 0):
    tot_v_values, tot_im_values = normalizeSignalValuesWithCalibration(id, limit)
    f = np.append(np.array(tot_v_values).flatten(), np.array(tot_im_values).flatten())
    return getPrediction(f, model)

def getPrediction(values, model):
    prediction = model.predict(values.reshape(1, -1))
    return prediction

def loadModel():
    filename = 'trained_model.sav'
    loaded_model = pickle.load(open(filename, 'rb'))
    return loaded_model

def trainModel():
    rf = RandomForestClassifier(n_estimators = 1000, random_state = 42)

    features, labels = getTrainingFeaturesAndLabels()
    rf.fit(features, labels)

    filename = 'trained_model.sav'
    pickle.dump(rf, open(filename, 'wb'))
    return

# USES 70% OF THE TRAINING TO DATA SET TO TRAIN AND 30% TO TEST ACCURACY
def trainModelWithTestSplit():
    rf = RandomForestClassifier(n_estimators = 1000, random_state = 42)

    features, labels = getTrainingFeaturesAndLabels()

    train_features, test_features, train_labels, test_labels = train_test_split(features, labels, test_size = 0.3)

    print(features.shape)

    print(train_features.shape)

    rf.fit(train_features, train_labels)

    pred_labels = rf.predict(test_features)

    print("ACCURACY OF THE MODEL: ", metrics.accuracy_score(test_labels, pred_labels))

    filename = 'trained_model.sav'
    pickle.dump(rf, open(filename, 'wb'))
    return

if __name__ == "__main__":
    # trainModel()
    # trainModelWithTestSplit()

    model = loadModel()
    print(getLatestPrediction(model, [1]))
    # print(getPredictionFromId(1, model, 11))