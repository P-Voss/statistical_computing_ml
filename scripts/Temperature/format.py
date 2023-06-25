import csv
import numpy
from datetime import datetime, timedelta

stations = [
    {"name": "Arkona", "file": "../../data/Temperature/Arkona/produkt_tu_termin_19470101_20221231_00183.txt", "data": {}},
    {"name": "Boltenhagen", "file": "../../data/Temperature/Boltenhagen/produkt_tu_termin_19470101_20221231_00596.txt","data": {}},
    {"name": "Cuxhaven", "file": "../../data/Temperature/Cuxhaven/produkt_tu_termin_19460101_20221231_00891.txt","data": {}},
    {"name": "Emden", "file": "../../data/Temperature/Emden/produkt_tu_termin_19970701_20221231_05839.txt","data": {}},
    {"name": "Fehmarn", "file": "../../data/Temperature/Fehmarn/produkt_tu_termin_19480101_20221231_05516.txt","data": {}},
    {"name": "Hattstedt", "file": "../../data/Temperature/Hattstedt/produkt_tu_termin_20050701_20221231_07298.txt","data": {}},
    {"name": "Hohwacht", "file": "../../data/Temperature/Hohwacht/produkt_tu_termin_19771101_20221231_02306.txt","data": {}},
    {"name": "Karlshagen", "file": "../../data/Temperature/Karlshagen/produkt_tu_termin_20040801_20221231_06310.txt","data": {}},
    {"name": "Konstanz", "file": "../../data/Temperature/Konstanz/produkt_tu_termin_19721101_20221231_02712.txt","data": {}},
    {"name": "Ploen", "file": "../../data/Temperature/Ploen/produkt_tu_termin_19500101_19970131_03955.txt","data": {}},
    {"name": "Prien", "file": "../../data/Temperature/Prien/produkt_tu_termin_19460101_19571231_04005.txt","data": {}},
    {"name": "Ueckermuende", "file": "../../data/Temperature/Ueckermuende/produkt_tu_termin_19360901_20221231_05142.txt","data": {}},
]

targetFileFormat = "../../data/Temperature/{}/formatted.csv"
trainingFileFormat = "training/{}/training.csv"

def getSeason(month):
    if month == 1 or month == 2 or month == 12:
        return 4
    if month == 3 or month == 4 or month == 5:
        return 1
    if month == 6 or month == 7 or month == 8:
        return 2
    return 3

def to_date_time(date_str):
    return datetime.strptime(date_str, '%Y%m%d%H')

def check_time_difference(current_time, prev_time):
    if prev_time is None:
        return False

    time_diff = current_time - prev_time
    if time_diff <= timedelta(hours=36):
        return True
    return False

productHeader = ["year", "month", "day", "hour", "value"]
trainingHeader = ["season", "year", "month", "day", "hour", "hour_sin", "hour_cos", "prev_temp", "value"]

for station in stations:
    # Bereite Zieldatei für formatierte Daten vor
    with open(targetFileFormat.format(station["name"]), 'w', newline='') as writeFile:
        writer = csv.writer(writeFile, delimiter=";")
        writer.writerow(productHeader)

        # Lese Quelldatei für Stationen aus
        with open(station["file"], 'r') as readFile:
            reader = csv.reader(readFile, delimiter=';')
            headers = next(reader)
            data = [{h: x.strip() for (h, x) in zip(headers, row)} for row in reader]
            for index, row in enumerate(data):

                formattedData = (
                    int(row["MESS_DATUM"][0:4]),
                    int(row["MESS_DATUM"][4:6]),
                    int(row["MESS_DATUM"][6:8]),
                    int(row["MESS_DATUM"][8:10]),
                    float(row["TT_TER"])
                )
                writer.writerow(formattedData)

    # Bereite Zieldatei für formatierte Daten vor
    with open(trainingFileFormat.format(station["name"]), 'w', newline='') as writeFile:
        writer = csv.writer(writeFile, delimiter=";")
        writer.writerow(trainingHeader)

        prev_temp = None
        prev_time = None

        # Lese Quelldatei für Stationen aus
        with open(station["file"], 'r') as readFile:
            reader = csv.reader(readFile, delimiter=';')
            headers = next(reader)
            data = [{h: x.strip() for (h, x) in zip(headers, row)} for row in reader]
            for index, row in enumerate(data):

                if float(row["TT_TER"]) == -999:
                    continue

                current_time = to_date_time(row["MESS_DATUM"])
                prev_temp_to_use = prev_temp if check_time_difference(current_time, prev_time) else float(row["TT_TER"])

                formattedData = (
                    getSeason(int(row["MESS_DATUM"][4:6])),
                    int(row["MESS_DATUM"][0:4]),
                    int(row["MESS_DATUM"][4:6]),
                    int(row["MESS_DATUM"][6:8]),
                    int(row["MESS_DATUM"][8:10]),
                    numpy.sin(2 * numpy.pi * int(row["MESS_DATUM"][8:10]) / 24),
                    numpy.cos(2 * numpy.pi * int(row["MESS_DATUM"][8:10]) / 24),
                    prev_temp_to_use,
                    float(row["TT_TER"])
                )
                writer.writerow(formattedData)
                prev_temp = float(row["TT_TER"])  # set current temp as previous temp for the next iteration
                prev_time = current_time

