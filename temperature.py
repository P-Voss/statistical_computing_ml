import csv
from datetime import date, timedelta


# Multivariate Lineare Regression? Verlauf und Monat
def estimateEntry(entries, key):
    indexes = []
    values = []
    positionToComplete = 0

    for index, entry in enumerate(entries):
        if entry["MESS_DATUM"] == key:
            positionToComplete = index
            # values.append(0)
            continue
        if int(entry["N_TER"]) < 0:
            continue
        indexes.append(index)
        values.append(int(entry["N_TER"]))

    if len(values) == 0:
        print(key)
        print(entries)
        exit()

    x = np.array(indexes).reshape((-1, 1))
    y = values
    model = LinearRegression()
    model.fit(x, y)

    return min(max(int((model.intercept_ + model.coef_ * positionToComplete).round()), 0), 8)

def daterange(start_date, end_date):
    for n in range(int((end_date - start_date).days)):
        yield start_date + timedelta(n)


places = [
    {"station": "Arkona", "file": "data/Temperature/Arkona/produkt_tu_termin_19470101_20221231_00183.txt", "data": {}},
    {"station": "Boltenhagen", "file": "data/Temperature/Boltenhagen/produkt_tu_termin_19470101_20221231_00596.txt","data": {}},
    {"station": "Cuxhaven", "file": "data/Temperature/Cuxhaven/produkt_tu_termin_19460101_20221231_00891.txt","data": {}},
    {"station": "Emden", "file": "data/Temperature/Emden/produkt_tu_termin_19970701_20221231_05839.txt","data": {}},
    {"station": "Fehmarn", "file": "data/Temperature/Fehmarn/produkt_tu_termin_19480101_20221231_05516.txt","data": {}},
    {"station": "Hattstedt", "file": "data/Temperature/Hattstedt/produkt_tu_termin_20050701_20221231_07298.txt","data": {}},
    {"station": "Hohwacht", "file": "data/Temperature/Hohwacht/produkt_tu_termin_19771101_20221231_02306.txt","data": {}},
    {"station": "Karlshagen", "file": "data/Temperature/Karlshagen/produkt_tu_termin_20040801_20221231_06310.txt","data": {}},
    {"station": "Konstanz", "file": "data/Temperature/Konstanz/produkt_tu_termin_19721101_20221231_02712.txt","data": {}},
    {"station": "Plön", "file": "data/Temperature/Plön/produkt_tu_termin_19500101_19970131_03955.txt","data": {}},
    {"station": "Prien", "file": "data/Temperature/Prien/produkt_tu_termin_19460101_19571231_04005.txt","data": {}},
    {"station": "Ueckermuende", "file": "data/Temperature/Ueckermuende/produkt_tu_termin_19360901_20221231_05142.txt","data": {}},
]

resultFile = "data/Temperature/result.csv"
entries = {}
start_date = date(2012, 1, 1)
end_date = date(2022, 12, 31)

if __name__ == '__main__':

    # Initialisiert Datenbasis von Startdatum bis Enddatum 6-stündlich für jede Station
    # Werte werden mit -999 initialisiert, um fehlende Werte zu kennzeichnen
    for station in places:
        for single_date in daterange(start_date, end_date):
            station["data"][int(single_date.strftime("%Y%m%d") + "00")] = -999
            station["data"][int(single_date.strftime("%Y%m%d") + "06")] = -999
            station["data"][int(single_date.strftime("%Y%m%d") + "12")] = -999
            station["data"][int(single_date.strftime("%Y%m%d") + "18")] = -999

        # Lese Quelldatei für Stationen aus
        with open(station["file"], 'r') as csvfile:
            reader = csv.reader(csvfile, delimiter=';')
            headers = next(reader)
            data = [{h: x.strip() for (h, x) in zip(headers, row)} for row in reader]
            for row in data:

                # Überspringe Einträge die vor dem Startdatum liegen
                if int(row["MESS_DATUM"]) < int(start_date.strftime("%Y%m%d")) * 100:
                    continue
                station["data"][int(row["MESS_DATUM"])] = row["N_TER"]

    for single_date in daterange(start_date, end_date):
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
        # create the csv writer
        writer = csv.writer(file)
        writer.writerow(header)
        for key in entries:
            values = entries[key]
            values.insert(0, int(key))
            writer.writerow(values)
