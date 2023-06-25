import csv
from datetime import date, timedelta
import numpy as np
from sklearn.linear_model import LinearRegression


def daterange(startDate, endDate):
    for n in range(int((endDate - startDate).days)):
        yield startDate + timedelta(n)


def countInvalidData(entries):
    count = 0
    for entry in entries:
        if int(entry["value"]) < 0:
            count += 1
    return count

def estimateEntry(entries, key):
    indexes = []
    values = []
    positionToComplete = 0

    for index, entry in enumerate(entries):
        if entry["datetime"] == key:
            positionToComplete = index
            continue
        if int(entry["value"]) < 0:
            continue
        indexes.append(index)
        values.append(int(entry["value"]))

    if len(values) == 0:
        print(key)
        print(entries)
        exit()

    x = np.array(indexes).reshape((-1, 1))
    y = values
    model = LinearRegression()
    model.fit(x, y)

    return min(max(int((model.intercept_ + model.coef_ * positionToComplete).round()), 0), 8)


places = [
    {"station": "Arkona", "data": {}},
    {"station": "Boltenhagen", "data": {}},
    {"station": "Cuxhaven", "data": {}},
    {"station": "Emden", "data": {}},
    {"station": "Fehmarn", "data": {}},
    # {"station": "Hattstedt", "data": {}},
    # {"station": "Hohwacht", "data": {}},
    # {"station": "Karlshagen", "data": {}},
    {"station": "Konstanz", "data": {}},
    # {"station": "Plön", "data": {}},
    # {"station": "Prien", "data": {}},
    {"station": "Ueckermuende", "data": {}},
]

resultFile = "../../data/Cloudiness/result.csv"
entries = {}
startDate = date(2012, 1, 1)
endDate = date(2022, 12, 31)

if __name__ == '__main__':
    for station in places:
        # Lese Quelldatei für Stationen aus
        with open("../../data/Cloudiness/" + station["station"] + "/clean.csv", 'r') as cleanfile:
            reader = csv.reader(cleanfile, delimiter=';')
            headers = next(reader)
            data = [{h: x.strip() for (h, x) in zip(headers, row)} for row in reader]
            for index, row in enumerate(data):
                if int(row["value"]) < 0:
                    lowerBound = max(0, index - 5)
                    upperBound = min(len(data) - 1, index + 5)
                    cloneData = data[:]

                    # Prüfe wie viele der folgenden Datensätze valide Werte enthalten
                    # Verhindert, dass ganze Blöcke von Daten erraten werden
                    validationCheckData = cloneData[index: upperBound]
                    if countInvalidData(validationCheckData) > 3:
                        data[index]["value"] = estimatedValue
                        station["data"][int(row["datetime"])] = estimatedValue
                        continue

                    extractedData = cloneData[lowerBound:upperBound]
                    estimatedValue = estimateEntry(extractedData, row["datetime"])
                    data[index]["value"] = estimatedValue
                    station["data"][int(row["datetime"])] = estimatedValue
                    continue
                station["data"][int(row["datetime"])] = row["value"]
        # print(station)
        # exit()

    for single_date in daterange(startDate, endDate):
        date = single_date.strftime("%Y%m%d")
        entries[(date + "00")] = []
        entries[(date + "06")] = []
        entries[(date + "12")] = []
        entries[(date + "18")] = []
        for station in places:
            try:
                entries[(date + "00")].append(station["data"][int(date + "00")])
                entries[(date + "06")].append(station["data"][int(date + "06")])
                entries[(date + "12")].append(station["data"][int(date + "12")])
                entries[(date + "18")].append(station["data"][int(date + "18")])
            except KeyError:
                print("error")
                exit()

    header = [place['station'] for place in places]
    header.insert(0, "datetime")
    with open(resultFile, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(header)
        for key in entries:
            values = entries[key]
            values.insert(0, int(key))
            writer.writerow(values)
