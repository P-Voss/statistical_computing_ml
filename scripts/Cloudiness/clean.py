import csv
from datetime import date, timedelta

def daterange(startDate, endDate):
    for n in range(int((endDate - startDate).days)):
        yield startDate + timedelta(n)

places = [
    {"station": "Arkona", "file": "../../data/Cloudiness/Arkona/produkt_n_termin_19510101_20221231_00183.txt", "data": {}},
    {"station": "Boltenhagen", "file": "../../data/Cloudiness/Boltenhagen/produkt_n_termin_19470101_20221231_00596.txt","data": {}},
    {"station": "Cuxhaven", "file": "../../data/Cloudiness/Cuxhaven/produkt_n_termin_19460101_20221231_00891.txt","data": {}},
    {"station": "Emden", "file": "../../data/Cloudiness/Emden/produkt_n_termin_19970701_20221231_05839.txt","data": {}},
    {"station": "Fehmarn", "file": "../../data/Cloudiness/Fehmarn/produkt_n_termin_19480101_20221231_05516.txt","data": {}},
    # {"station": "Hattstedt", "file": "../../data/Cloudiness/Hattstedt/produkt_n_termin_20050701_20111231_07298.txt","data": {}},
    # {"station": "Hohwacht", "file": "../../data/Cloudiness/Hohwacht/produkt_n_termin_19771101_20111231_02306.txt","data": {}},
    # {"station": "Karlshagen", "file": "../../data/Cloudiness/Karlshagen/produkt_n_termin_20040801_20111231_06310.txt","data": {}},
    {"station": "Konstanz", "file": "../../data/Cloudiness/Konstanz/produkt_n_termin_19721101_20221231_02712.txt","data": {}},
    # {"station": "Plön", "file": "../../data/Cloudiness/Plön/produkt_n_termin_19500101_19970131_03955.txt","data": {}},
    # {"station": "Prien", "file": "../../data/Cloudiness/Prien/produkt_n_termin_19460101_19571231_04005.txt","data": {}},
    {"station": "Ueckermuende", "file": "../../data/Cloudiness/Ueckermuende/produkt_n_termin_19360901_20221231_05142.txt","data": {}},
]

resultFile = "result.csv"
entries = {}
startDate = date(2012, 1, 1)
endDate = date(2022, 12, 31)

if __name__ == '__main__':

    # Initialisiert Datenbasis von Startdatum bis Enddatum 6-stündlich für jede Station
    # Werte werden mit -999 initialisiert, um fehlende Werte zu kennzeichnen
    for station in places:
        for single_date in daterange(startDate, endDate):
            station["data"][int(single_date.strftime("%Y%m%d") + "00")] = -999
            station["data"][int(single_date.strftime("%Y%m%d") + "06")] = -999
            station["data"][int(single_date.strftime("%Y%m%d") + "12")] = -999
            station["data"][int(single_date.strftime("%Y%m%d") + "18")] = -999

        # Lese Quelldatei für Stationen aus
        with open(station["file"], 'r') as csvfile:
            reader = csv.reader(csvfile, delimiter=';')
            headers = next(reader)
            data = [{h: x.strip() for (h, x) in zip(headers, row)} for row in reader]
            for index, row in enumerate(data):
                # Überspringe Einträge die vor dem Startdatum liegen
                if int(row["MESS_DATUM"]) < int(startDate.strftime("%Y%m%d")) * 100:
                    continue
                station["data"][int(row["MESS_DATUM"])] = row["N_TER"]

    for station in places:
        header = ["datetime", "value"]
        with open("../../data/Cloudiness/" + station["station"] + "/clean.csv", 'w', newline='') as file:
            # create the csv writer
            writer = csv.writer(file, delimiter=";")
            writer.writerow(header)

            for (datetime, value) in station["data"].items():
                values = [datetime, value]
                writer.writerow(values)

