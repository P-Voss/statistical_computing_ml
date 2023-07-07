
import pandas
import numpy as np
import tensorflow.python.keras.models
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense
from tensorflow.keras.callbacks import EarlyStopping
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from tensorflow.keras.callbacks import ModelCheckpoint
import joblib

class WindRNN:

    def __init__(self):
        self.model = None

    def initiateModel(self):
        self.model = Sequential()
        self.model.compile(loss='mean_squared_error', optimizer='adam', metrics=['mean_absolute_error'])


    def executeTraining(self, trainingfile, checkpointfile, scalerfile):
        data = pandas.read_csv(trainingfile, delimiter=';')
        data = pandas.get_dummies(data, columns=['season'])

        # Zieldaten
        target = data['wind_str']

        # Feature Daten
        features = data[['season_1', 'season_2', 'season_3', 'season_4', 'year', 'month', 'day', 'hour_sin', 'hour_cos',
                         'prev_temp', 'prev_hum', 'humidity', 'temp', 'wind_dir', 'coverage', 'range', 'prec']]

        # scaler = StandardScaler()
        scaler = MinMaxScaler()
        features = scaler.fit_transform(features)

        joblib.dump(scaler, scalerfile)

        # Umwandlung der Daten in 3D-Format für LSTMs
        features = np.reshape(features, (features.shape[0], 1, features.shape[1]))

        features_train, features_test, target_train, target_test = train_test_split(
            features, target, test_size=0.2, random_state=42
        )

        if self.model is None:
            self.initiateModel()

        self.model.add(LSTM(128, activation='relu', input_shape=(features_train.shape[1], features_train.shape[2])))

        self.model.add(Dense(128, activation='relu'))
        self.model.add(Dense(1))

        checkpoint = ModelCheckpoint(
            checkpointfile,
            monitor='val_loss',
            verbose=1,
            save_best_only=True,
            mode='min'
        )

        # Training des Modells
        early_stop = EarlyStopping(monitor='val_mean_absolute_error', patience=15)

        history = self.model.fit(
            features_train,
            target_train,
            validation_data=(features_test, target_test),
            epochs=500,
            batch_size=128,
            callbacks=[early_stop, checkpoint]
        )

        predictions = self.model.predict(features_test)
        errors = predictions.flatten() - target_test.to_numpy()
        std_deviation = np.std(errors)

        return {
            'mae': min(history.history['val_mean_absolute_error']),
            'stdDev': std_deviation,
            'errors': errors
        }

    def loadModel(self, path):
        self.model = tensorflow.python.keras.models.load_model(path)

    def resetModel(self, path):
        self.model = None

    def saveModel(self, path):
        if self.model is not None:
            self.model.save(path)
        else:
            print("No model to save.")
