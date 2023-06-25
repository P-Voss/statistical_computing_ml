import csv
from datetime import date, timedelta


def daterange(start_date, end_date):
    for n in range(int((end_date - start_date).days)):
        yield start_date + timedelta(n)


places = [
    {"station": "Arkona", "file": "data/Range/Arkona/produkt_vk_termin_19510101_20221231_00183.txt", "data": {}},
    {"station": "Boltenhagen", "file": "data/Range/Boltenhagen/produkt_vk_termin_19470101_20221231_00596.txt","data": {}},
    {"station": "Cuxhaven", "file": "data/Range/Cuxhaven/produkt_vk_termin_19460101_20221231_00891.txt","data": {}},
    {"station": "Emden", "file": "data/Range/Emden/produkt_vk_termin_19970701_20221231_05839.txt","data": {}},
    {"station": "Fehmarn", "file": "data/Range/Fehmarn/produkt_vk_termin_19480101_20221231_05516.txt","data": {}},
    {"station": "Hattstedt", "file": "data/Range/Hattstedt/produkt_vk_termin_20050701_20111231_07298.txt","data": {}},
    {"station": "Hohwacht", "file": "data/Range/Hohwacht/produkt_vk_termin_19771101_20111231_02306.txt","data": {}},
    {"station": "Karlshagen", "file": "data/Range/Karlshagen/produkt_vk_termin_20040801_20111231_06310.txt","data": {}},
    {"station": "Konstanz", "file": "data/Range/Konstanz/produkt_vk_termin_19721101_20221231_02712.txt","data": {}},
    {"station": "Plön", "file": "data/Range/Plön/produkt_vk_termin_19500101_19970131_03955.txt","data": {}},
    {"station": "Prien", "file": "data/Range/Prien/produkt_vk_termin_19460101_19571231_04005.txt","data": {}},
    {"station": "Ueckermuende", "file": "data/Range/Ueckermuende/produkt_vk_termin_19510101_20221231_05142.txt","data": {}},
]

resultFile = "data/Range/result.csv"
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
