import json
import numpy
from pathlib import Path
from WindRNN import WindRNN

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
    {"name": "Ueckermünde", "file": "Ueckermuende"},
]

trainingFileFormat = "../../data/training/{}_training.csv"
errorsFileFormat = "training/{}/errors.npy"
modelFileFormat = "training/{}/model.h5"
checkpointFileFormat = "training/{}/checkpoint.h5"
scalerFileFormat = "training/{}/scaler.pkl"
reportFile = "training/wind_report.json"
reports = {}

for station in stations:

    modelFilePath = Path(modelFileFormat.format(station['file']))
    # if modelFilePath.is_file():
    #     print("Model for " + station["name"] + " already exists. Skipping to the next station.")
    #     continue

    trainingFilePath = Path(trainingFileFormat.format(station["file"]))
    if not trainingFilePath.is_file():
        print("No training data found for " + station["name"] + ". Skipping to the next station.")
        continue

    Rnn = WindRNN()
    print("--- Running Training for " + station['name'] + " ---")

    result = Rnn.executeTraining(
        trainingFileFormat.format(station["file"]),
        checkpointFileFormat.format(station["file"]),
        scalerFileFormat.format(station["file"])
    )

    print("--- Result " + station['name'] + " ---")
    print("MAE: " + str(result['mae']))
    print("Standardabweichung der Fehler: " + str(result['stdDev']))
    reports[station['file']] = {'mae': result['mae'], 'stdDev': result['stdDev']}
    numpy.save(errorsFileFormat.format(station['file']), result['errors'])

    print("Saving Model for station " + station["name"])
    Rnn.saveModel(modelFileFormat.format(station['file']))

with open(reportFile, 'w') as file:
    json.dump(reports, file)
