
import tensorflow as tf
import pandas
import matplotlib.pyplot as plt
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from tensorflow.keras.wrappers.scikit_learn import KerasClassifier
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import KFold
from tensorflow.keras.utils import to_categorical

stations = [
    {"name": "Arkona", "data": {}},
    {"name": "Boltenhagen", "data": {}},
    {"name": "Cuxhaven", "data": {}},
    {"name": "Emden", "data": {}},
    {"name": "Fehmarn", "data": {}},
    {"name": "Hattstedt", "data": {}},
    {"name": "Hohwacht", "data": {}},
    {"name": "Karlshagen", "data": {}},
    {"name": "Konstanz", "data": {}},
    {"name": "Plön", "data": {}},
    {"name": "Prien", "data": {}},
    {"name": "Ueckermuende", "data": {}},
]

trainingFileFormat = "training/{}/training.csv"
modelFileFormat = "training/{}/model.h5"


def create_model():
    model = tf.keras.models.Sequential([
        tf.keras.layers.Dense(16, activation='relu', input_shape=(3,)),
        tf.keras.layers.Dense(8, activation='relu'),
        tf.keras.layers.Dense(9, activation='softmax')
    ])

    model.compile(loss='categorical_crossentropy',
                  optimizer='adam',
                  metrics=['accuracy'])
    return model

n_folds = 5
kfold = KFold(n_folds, shuffle=True, random_state=42)

for station in stations:

    histories = []

    fold_number = 1

    data = pandas.read_csv(trainingFileFormat.format(station['name']), delimiter=';')
    features = data[['month', 'day', 'hour']]
    # features = data[['year', 'month', 'day', 'hour']]
    # Zieldaten
    target = data['value']

    # one-hot kodierte Zieldaten
    # target = pandas.get_dummies(data['value'])

    # Skalierung der Feature-Daten
    scaler = StandardScaler()
    features = scaler.fit_transform(features)

    # Stellen Sie sicher, dass die Ziele auf einer Skala von 0 bis 8 liegen und dass sie kategorial kodiert sind
    target = to_categorical(target)

    model = create_model()

    for train_index, val_index in kfold.split(features, target):
        features_train, features_val = features[train_index], features[val_index]
        target_train, target_val = target[train_index], target[val_index]

        print(f'---- Starting training for Fold {fold_number} ----')

        history = model.fit(
            features_train,
            target_train,
            epochs=20,  # Run one epoch at a time
            batch_size=64,
            validation_data=(features_val, target_val),
            verbose=1)

        fold_number += 1

    exit("done")

