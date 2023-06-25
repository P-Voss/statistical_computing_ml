
# Skript to develop and test the RNN network on a single station

import pandas
import numpy as np
import matplotlib.pyplot as plt
import tensorflow.python.keras.layers
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense
from tensorflow.keras.callbacks import EarlyStopping
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler


trainingFileFormat = "training/Arkona/training.csv"
modelFileFormat = "training/Arkona/model.h5"

data = pandas.read_csv(trainingFileFormat, delimiter=';')
data = pandas.get_dummies(data, columns=['season'])

# Zieldaten
target = data['value']

# Feature Daten
features = data[['season_1','season_2', 'season_3', 'season_4', 'year', 'month', 'day']]
scaler = StandardScaler()
features = scaler.fit_transform(features)

# Umwandlung der Daten in 3D-Format für LSTMs
features = np.reshape(features, (features.shape[0], 1, features.shape[1]))

features_train, features_test, target_train, target_test = train_test_split(
    features, target, test_size=0.2, random_state=42
)

model = Sequential()
model.add(LSTM(128, activation='relu', input_shape=(features_train.shape[1], features_train.shape[2])))
model.add(tensorflow.keras.layers.Dropout(0.2))
model.add(Dense(1))

model.compile(loss='mean_squared_error', optimizer='adam', metrics=['mean_absolute_error'])

# Training des Modells
early_stop = EarlyStopping(monitor='val_loss', patience=10)

history = model.fit(
    features_train,
    target_train,
    validation_data=(features_test, target_test),
    epochs=500,
    batch_size=256,
    callbacks=[early_stop]
)

model.save(modelFileFormat)

# Visualisierung der Ergebnisse
plt.figure(figsize=(12, 4))

plt.subplot(1, 2, 1)
plt.plot(history.history['loss'], label='Trainingsverlust')
plt.plot(history.history['val_loss'], label='Validierungsverlust')
plt.legend()

plt.subplot(1, 2, 2)
plt.plot(history.history['mean_absolute_error'], label='Trainingsgenauigkeit')
plt.plot(history.history['val_mean_absolute_error'], label='Validierungsgenauigkeit')
plt.legend()

plt.show()
