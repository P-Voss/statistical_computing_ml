
# 1) Skript führt den vorhandenen Daten die Messpunkte zum Niederschlag zu
# Niederschlag u.A. wird stündlich erfasst, hier können daraus verschiedene Faktoren erstellt werden, z.B.
# - Tageswert
# - Wert zum Messzeitpunkt (der anderen Faktoren)
# - Niederschlag der letzten X Stunden
# 2) Ergänzt die Daten außerdem um die Jahreszeit und Temperaturdaten des Vortags, codiert die Uhrzeit des Messdatums
# 3) Wandelt Kürzel des DWD zu sprechenden Bezeichnungen um, z.B. RF_TER => humidity

import csv
import numpy
import pandas
from datetime import datetime, timedelta

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


def getMetricWindStr(val):
    beaufortScale = {
        0: (0, 0.2),
        1: (0.3, 1.5),
        2: (1.6, 3.3),
        3: (3.4, 5.4),
        4: (5.5, 7.9),
        5: (8.0, 10.7),
        6: (10.8, 13.8),
        7: (13.9, 17.1),
        8: (17.2, 20.7),
        9: (20.8, 24.4),
        10: (24.5, 28.4),
        11: (28.5, 32.6),
        12: (32.7, 40),
    }

    for key, (lower, upper) in beaufortScale.items():
        if key == int(float(val)):
            return (lower + upper) / 2

def to_date_time(date_str):
    return datetime.strptime(date_str, '%Y%m%d%H')

def check_time_difference(current_time, prev_time):
    if prev_time is None:
        return False

    time_diff = current_time - prev_time
    if time_diff <= timedelta(hours=36):
        return True
    return False

stations = [
    {'name': 'Arkona'},
    {'name': 'Boltenhagen'},
    {'name': 'Cuxhaven'},
    {'name': 'Emden'},
    {'name': 'Fehmarn'},
    {'name': 'Hattstedt'},
    {'name': 'Hohwacht'},
    {'name': 'Karlshagen'},
    {'name': 'Konstanz'},
    {'name': 'Ueckermuende'},
]

filteredFileFormat = '../data/training/{}_filtered.csv'
trainingFileFormat = '../data/training/{}_training.csv'
rainFileFormat = '../data/source/Rain/{}/product.txt'

for station in stations:
    # RS = Tageswert Niederschlag
    rainDf = pandas.read_csv(rainFileFormat.format(station['name']), delimiter=';', skipinitialspace=True, usecols=['MESS_DATUM', 'RS'], dtype={'MESS_DATUM': str})
    rainDf.set_index('MESS_DATUM', inplace=True)
    rainDf.index.str.strip()

    with open(filteredFileFormat.format(station['name']), 'r') as csv_file:
        reader = csv.DictReader(csv_file, delimiter=';')
        formatted_data = []

        prev_temp = None
        prev_hum = None
        prev_time = None

        for row in reader:
            current_time = to_date_time(row["MESS_DATUM"])
            prev_temp_to_use = prev_temp if check_time_difference(current_time, prev_time) else float(row["TT_TER"])
            prev_hum = prev_hum if check_time_difference(current_time, prev_time) else float(row["RF_TER"])

            if row["MESS_DATUM"][0:8] in rainDf.index:
                rain = rainDf.at[row["MESS_DATUM"][0:8], 'RS']
            else:
                continue

            formatted_row = (
                row["MESS_DATUM"],
                int(getSeason(int(row["MESS_DATUM"][4:6]))),
                int(row["MESS_DATUM"][0:4]),
                int(row["MESS_DATUM"][4:6]),
                int(row["MESS_DATUM"][6:8]),
                int(row["MESS_DATUM"][8:10]),
                numpy.sin(2 * numpy.pi * int(row["MESS_DATUM"][8:10]) / 24),
                numpy.cos(2 * numpy.pi * int(row["MESS_DATUM"][8:10]) / 24),
                prev_temp_to_use,
                prev_hum,
                float(row["TT_TER"]),
                float(row["RF_TER"]),
                getCoverageClass(int(float(row["N_TER"]))),
                int(float(row["N_TER"])),
                float(row["N_TER"]) * 12.5,
                float(row["VK_TER"]),
                float(row["DK_TER"]),
                float(row["FK_TER"]),
                float(getMetricWindStr(row["FK_TER"])),
                float(rain),
            )
            formatted_data.append(formatted_row)

            prev_temp = float(row["TT_TER"])  # set current temp as previous temp for the next iteration
            prev_hum = float(row["RF_TER"])  # set current humidity as previous humidity for the next iteration
            prev_time = current_time
    header = [
        'MESS_DATUM',
        'season',
        'year',
        'month',
        'day',
        'hour',
        'hour_sin',
        'hour_cos',
        'prev_temp',
        'prev_hum',
        'temp',
        'humidity',
        'coverage_class',
        'coverage',
        'coverage_percent',
        'range',
        'wind_dir',
        'wind_str',
        'wind_str_metric',
        'prec'
    ]
    with open(trainingFileFormat.format(station['name']), 'w', newline='') as csv_file:
        writer = csv.writer(csv_file, delimiter=';')
        writer.writerow(header)
        writer.writerows(formatted_data)
