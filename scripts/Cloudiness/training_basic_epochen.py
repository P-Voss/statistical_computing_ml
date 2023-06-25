
import tensorflow as tf
import pandas
import matplotlib.pyplot as plt
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

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

for station in stations:
    data = pandas.read_csv(trainingFileFormat.format(station['name']), delimiter=';')
    features = data[['month', 'day', 'hour']]
    # features = data[['year', 'month', 'day', 'hour']]
    # Zieldaten
    # target = data['value']

    # one-hot kodierte Zieldaten
    target = pandas.get_dummies(data['value'])

    # Skalierung der Feature-Daten
    scaler = StandardScaler()
    features = scaler.fit_transform(features)

    features_train, features_test, target_train, target_test = train_test_split(
        features, target, test_size=0.1, random_state=42
    )

    # Initialisieren des neuronalen Netzwerks
    model = tf.keras.models.Sequential([
        tf.keras.layers.Dense(32, activation='relu', input_shape=(3,)),
        tf.keras.layers.Dense(32, activation='relu'),
        # tf.keras.layers.Dense(64, activation='relu'),
        tf.keras.layers.Dense(9, activation='softmax'),
    ])

    model.compile(
        optimizer='adam',
        loss='categorical_crossentropy',
        metrics=['accuracy']
    )

    batchSize = 64
    epochs = 100
    history = model.fit(
        features_train,
        target_train,
        validation_data=(features_test, target_test),
        batch_size=batchSize,
        epochs=epochs
    )
    model.save(modelFileFormat.format(station['name']))

    plt.figure(figsize=(12, 4))

    plt.subplot(1, 2, 1)
    plt.plot(history.history['loss'], label='Trainingsverlust')
    plt.plot(history.history['val_loss'], label='Validierungsverlust')
    plt.legend()

    plt.subplot(1, 2, 2)
    plt.plot(history.history['accuracy'], label='Trainingsgenauigkeit')
    plt.plot(history.history['val_accuracy'], label='Validierungsgenauigkeit')
    plt.legend()

    plt.show()

    # model.summary()
    exit("done")

