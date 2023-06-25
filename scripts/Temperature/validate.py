import json
from pathlib import Path
import tensorflow.python.keras.models
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_absolute_error

stations = [
    {"name": "Arkona", "file": "Arkona"},
    {"name": "Boltenhagen", "file": "Boltenhagen"},
    {"name": "Cuxhaven", "file": "Cuxhaven"},
    {"name": "Emden", "file": "Emden"},
    {"name": "Fehmarn", "file": "Fehmarn"},
    {"name": "Hattstedt", "file": "Hattstedt"},
    {"name": "Hohwacht", "file": "Hohwacht"},
    {"name": "Karlshagen", "file": "Karlshagen"},
    {"name": "Konstanz", "file": "Konstanz"},
    {"name": "Plön", "file": "Ploen"},
    {"name": "Prien", "file": "Prien"},
    {"name": "Ueckermünde", "file": "Ueckermuende"},
]

trainingFileFormat = "training/{}/training.csv"
modelFileFormat = "training/{}/model.h5"
checkpointFileFormat = "training/{}/checkpoint.h5"
reportFile = "training/mae_report.json"
reports = {}

for station in stations:

    modelFilePath = Path(modelFileFormat.format(station['file']))
    if not modelFilePath.is_file():
        print("Model for " + station["name"] + " does not exist. Skipping to the next station.")
        continue

    trainingFilePath = Path(trainingFileFormat.format(station["file"]))
    if not trainingFilePath.is_file():
        print("No training data found for " + station["name"] + ". Skipping to the next station.")
        continue
    try:
        data = pd.read_csv(trainingFileFormat.format(station["file"]), delimiter=';')
        data = pd.get_dummies(data, columns=['season'])

        # Zieldaten
        labels = data['value']

        # Feature Daten
        features = data[
            ['season_1', 'season_2', 'season_3', 'season_4', 'year', 'month', 'day', 'hour_sin', 'hour_cos', 'prev_temp']
        ]
        scaler = StandardScaler()
        features = scaler.fit_transform(features)

        # Umwandlung der Daten in 3D-Format für LSTM
        features = np.reshape(features, (features.shape[0], 1, features.shape[1]))

        test_features = features
        test_labels = labels

        model = tensorflow.keras.models.load_model(modelFileFormat.format(station['file']))

        # Vorhersagen mit dem Modell machen
        predicted_labels = model.predict(test_features)

        print("--- Running Test for " + station['name'] + " ---")
        result = mean_absolute_error(test_labels, predicted_labels)

        print("--- Result " + station['name'] + " ---")
        print("MAE: " + str(result))
        reports[station['name']] = result

    except Exception as e:
        import traceback
        print("Ein Fehler ist aufgetreten:")
        print(traceback.format_exc())

print("Alle Ergebnisse")
print(reports)

# with open(reportFile, 'w') as file:
#     json.dump(reports, file)
