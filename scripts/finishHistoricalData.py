
# Skript prüft, ob historische Daten für alle Tage in der Zeitspanne vorhanden sind
# Trifft für die 10 Wetterstationen zu, ansonsten müsste das Skript erweitert werden, um die Lücken
# mit Trend- oder typischen Daten zu schließen

import pandas

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

trendFileFormat = '../data/trend/{}.csv'
dataFileFormat = '../data/history/{}.csv'
completedFileFormat = '../data/completed/{}.csv'

for station in stations:
    data = pandas.read_csv(dataFileFormat.format(station['name']), sep=';', dtype={'MESS_DATUM': str})

    data.columns = ['date', 'coverage', 'range', 'temp', 'humidity', 'wind_dir', 'wind_str']
    data['date'] = pandas.to_datetime(data['date'], format='%Y%m%d%H')

    data['date'] = data['date'].dt.date

    date_range = pandas.date_range(start="20190101", end="20221231", freq='D')
    full_data = pandas.DataFrame(date_range, columns=['date'])
    full_data['date'] = full_data['date'].dt.date

    data['original'] = True

    merged = pandas.merge(full_data, data, how='left', on='date')
    merged['original'].fillna(False, inplace=True)
    merged.fillna(0, inplace=True)

    merged.to_csv(completedFileFormat.format(station['name']), sep=';', index=False)
