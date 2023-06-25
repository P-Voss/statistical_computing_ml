import csv

stations = [
    {"name": "Arkona", "file": "../../data/Cloudiness/Arkona/produkt_n_termin_19510101_20221231_00183.txt", "data": {}},
    {"name": "Boltenhagen", "file": "../../data/Cloudiness/Boltenhagen/produkt_n_termin_19470101_20221231_00596.txt","data": {}},
    {"name": "Cuxhaven", "file": "../../data/Cloudiness/Cuxhaven/produkt_n_termin_19460101_20221231_00891.txt","data": {}},
    {"name": "Emden", "file": "../../data/Cloudiness/Emden/produkt_n_termin_19970701_20221231_05839.txt","data": {}},
    {"name": "Fehmarn", "file": "../../data/Cloudiness/Fehmarn/produkt_n_termin_19480101_20221231_05516.txt","data": {}},
    {"name": "Hattstedt", "file": "../../data/Cloudiness/Hattstedt/produkt_n_termin_20050701_20111231_07298.txt","data": {}},
    {"name": "Hohwacht", "file": "../../data/Cloudiness/Hohwacht/produkt_n_termin_19771101_20111231_02306.txt","data": {}},
    {"name": "Karlshagen", "file": "../../data/Cloudiness/Karlshagen/produkt_n_termin_20040801_20111231_06310.txt","data": {}},
    {"name": "Konstanz", "file": "../../data/Cloudiness/Konstanz/produkt_n_termin_19721101_20221231_02712.txt","data": {}},
    {"name": "Ploen", "file": "../../data/Cloudiness/Ploen/produkt_n_termin_19500101_19970131_03955.txt","data": {}},
    {"name": "Prien", "file": "../../data/Cloudiness/Prien/produkt_n_termin_19460101_19571231_04005.txt","data": {}},
    {"name": "Ueckermuende", "file": "../../data/Cloudiness/Ueckermuende/produkt_n_termin_19360901_20221231_05142.txt","data": {}},
]

targetFileFormat = "../../data/Cloudiness/{}/formatted.csv"
trainingFileFormat = "training/{}/training.csv"

def getSeason(month):
    if month == 1 or month == 2 or month == 12:
        return 4
    if month == 3 or month == 4 or month == 5:
        return 1
    if month == 6 or month == 7 or month == 8:
        return 2
    return 3

def getCoverageClass(value):
    if value == 0:
        return 0
    elif 1 <= value <= 3:
        return 1
    elif 4 <= value <= 6:
        return 2
    elif value == 7:
        return 3
    else:
        return 4

for station in stations:
    # Bereite Zieldatei für formatierte Daten vor
    header = ["year", "month", "day", "hour", "value"]
    with open(targetFileFormat.format(station["name"]), 'w', newline='') as writeFile:
        writer = csv.writer(writeFile, delimiter=";")
        writer.writerow(header)

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
                    int(row["N_TER"])
                )
                writer.writerow(formattedData)

    # Bereite Zieldatei für formatierte Daten vor
    header = ["season", "year", "month", "day", "hour", "class", "value"]
    with open(trainingFileFormat.format(station["name"]), 'w', newline='') as writeFile:
        writer = csv.writer(writeFile, delimiter=";")
        writer.writerow(header)

        # Lese Quelldatei für Stationen aus
        with open(station["file"], 'r') as readFile:
            reader = csv.reader(readFile, delimiter=';')
            headers = next(reader)
            data = [{h: x.strip() for (h, x) in zip(headers, row)} for row in reader]
            for index, row in enumerate(data):

                if int(row["N_TER"]) == -999:
                    continue

                formattedData = (
                    getSeason(int(row["MESS_DATUM"][4:6])),
                    int(row["MESS_DATUM"][0:4]),
                    int(row["MESS_DATUM"][4:6]),
                    int(row["MESS_DATUM"][6:8]),
                    int(row["MESS_DATUM"][8:10]),
                    getCoverageClass(int(row["N_TER"])),
                    int(row["N_TER"])
                )
                writer.writerow(formattedData)

