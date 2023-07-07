from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv1D, MaxPooling1D, Flatten, Dense
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from tensorflow.keras.utils import to_categorical
import joblib
import pandas
import numpy as np

class CloudinessCNN:

    def __init__(self):
        self.model = None

    def initiateModel(self):
        self.model = Sequential()
        self.model.add(Conv1D(filters=32, kernel_size=1, activation='relu', input_shape=(1, 16)))
        self.model.add(Conv1D(filters=64, kernel_size=1, activation='relu'))
        self.model.add(Flatten())
        self.model.add(Dense(50, activation='relu'))
        self.model.add(Dense(1))
        self.model.compile(optimizer='adam', loss='mean_squared_error', metrics=['mean_squared_error'])

    def executeTraining(self, trainingfile, checkpointfile, scalerfile):
        data = pandas.read_csv(trainingfile, delimiter=';')
        data = pandas.get_dummies(data, columns=['season'])

        # Zieldaten
        target = data['coverage']
        # target = to_categorical(target)

        # Feature Daten
        features = data[['season_1', 'season_2', 'season_3', 'season_4', 'year', 'month', 'day', 'hour_sin', 'hour_cos',
                         'prev_temp', 'prev_hum', 'humidity', 'temp', 'wind_dir', 'wind_str', 'prec']]

        scaler = StandardScaler()
        features = scaler.fit_transform(features)

        joblib.dump(scaler, scalerfile)

        # Umwandlung der Daten in 3D-Format für CNN
        features = np.reshape(features, (features.shape[0], 1, features.shape[1]))

        features_train, features_test, target_train, target_test = train_test_split(
            features, target, test_size=0.2, random_state=42
        )

        if self.model is None:
            self.initiateModel()

        checkpoint = ModelCheckpoint(
            checkpointfile,
            monitor='val_loss',
            verbose=1,
            save_best_only=True,
            mode='min'
        )

        # Training des Modells
        early_stop = EarlyStopping(monitor='mean_squared_error', patience=15)

        history = self.model.fit(
            features_train,
            target_train,
            validation_data=(features_test, target_test),
            epochs=500,
            batch_size=256,
            callbacks=[early_stop, checkpoint]
        )
        return min(history.history['mean_squared_error'])

    def loadModel(self, path):
        self.model = tensorflow.keras.models.load_model(path)

    def resetModel(self, path):
        self.model = None

    def saveModel(self, path):
        if self.model is not None:
            self.model.save(path)
        else:
            print("No model to save.")