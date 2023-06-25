
# Skript to develop and test the network on a single station, using dense neuron layers

import tensorflow as tf
import pandas
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from tensorflow.keras.callbacks import EarlyStopping
from tensorflow.keras import regularizers


trainingFileFormat = "training/Arkona/training.csv"
modelFileFormat = "training/Arkona/model.h5"

data = pandas.read_csv(trainingFileFormat, delimiter=';')
data = pandas.get_dummies(data, columns=['season'])

# Und dann die `features` aktualisieren:
features = data[['season_1', 'season_2', 'season_3', 'season_4',
                 'month',
                 'year', 'day', 'hour_sin', 'hour_cos', 'prev_temp']]


# Skalierung der Feature-Daten
scaler = StandardScaler()
features = scaler.fit_transform(features)

# Zieldaten
target = data['value']

features_train, features_test, target_train, target_test = train_test_split(
    features, target, test_size=0.2, random_state=42
)

# Initialisieren des neuronalen Netzwerks
model = tf.keras.models.Sequential([
    # tf.keras.layers.Dense(32, activation='relu', input_shape=(4,)),
    tf.keras.layers.Dense(256, activation='relu', input_shape=(10,), kernel_regularizer=regularizers.l2(0.01)),
    tf.keras.layers.Dense(64, activation='relu', kernel_regularizer=regularizers.l1(0.01)), # L1 regularization
    tf.keras.layers.Dropout(0.2),
    tf.keras.layers.Dense(128, activation='relu'),
    tf.keras.layers.Dense(64, activation='relu', kernel_regularizer=regularizers.l1(0.01)), # L1 regularization
    # tf.keras.layers.Dropout(0.2),
    tf.keras.layers.Dense(64, activation='relu'),
    tf.keras.layers.Dense(1),
])

model.compile(
    optimizer='adam',
    loss='mean_squared_error',
    metrics=['mean_absolute_error']
)

batchSize = 256
epochs = 500

# Define the early stopping criteria
early_stop = EarlyStopping(monitor='val_loss', patience=20)

history = model.fit(
    features_train,
    target_train,
    validation_data=(features_test, target_test),
    batch_size=batchSize,
    epochs=epochs,
    callbacks=[early_stop]
)
model.save(modelFileFormat)

plt.figure(figsize=(12, 4))

plt.subplot(1, 2, 1)
plt.plot(history.history['loss'], label='Trainingsverlust')
plt.plot(history.history['val_loss'], label='Validierungsverlust')
plt.legend()

plt.subplot(1, 2, 2)
plt.plot(history.history['mean_absolute_error'], label='Trainingsfehler')
plt.plot(history.history['val_mean_absolute_error'], label='Validierungsfehler')
plt.legend()

plt.show()

