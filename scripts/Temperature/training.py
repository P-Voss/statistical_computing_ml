import json
from pathlib import Path
from TemperatureRNN import TemperatureRNN

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

trainingFileFormat = "../../training/{}_training.csv"
modelFileFormat = "training/{}/model.h5"
checkpointFileFormat = "training/{}/checkpoint.h5"
scalerFileFormat = "training/{}/scaler.pkl"
reportFile = "training/temperature_report.json"
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

    Rnn = TemperatureRNN()
    print("--- Running Training for " + station['name'] + " ---")

    result = Rnn.executeTraining(
        trainingFileFormat.format(station["file"]),
        checkpointFileFormat.format(station["file"]),
        scalerFileFormat.format(station["file"])
    )

    print("--- Result " + station['name'] + " ---")
    print("MAE: " + str(result))
    reports[station['file']] = result

    if result < 2.5:
        print("Saving Model for station " + station["name"])
        Rnn.saveModel(modelFileFormat.format(station['file']))
    else:
        print("Zu große Abweichung von den Zielwerten. Modell für " + station["name"] + " muss angepasst werden.")

with open(reportFile, 'w') as file:
    json.dump(reports, file)
