
# Skript bildet pro Wetterstation Durchschnittswerte für jeden Tag des Jahres anhand der historischen Daten
# Trend, bzw. typischer Wert, dient der Vorhersage per AI-Modell und als Vergleichswert in Visualisierung

import pandas as pd

importFileFormat = '../data/training/{}_training.csv'
trendFileFormat = '../data/trend/{}.csv'

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

for station in stations:
    df = pd.read_csv(importFileFormat.format(station['name']), delimiter=";")

    # Datumsspalte in ein datetime-Objekt umwandeln und den Tag und die Stunde extrahieren
    date = pd.to_datetime(df['MESS_DATUM'], format='%Y%m%d%H')
    df['date'] = date.dt.strftime('%m%d%H')

    # Entferne Daten die später abgeleitet werden können
    data = df.drop(columns=['hour_sin', 'hour_cos', 'season', 'year', 'month', 'day', 'hour', 'coverage_class', 'MESS_DATUM'])
    # Durchschnitt pro Tag und Stunde berechnen
    data = data.groupby('date').mean()

    # Werte runden
    data[['coverage', 'wind_dir', 'wind_str']] = data[['coverage', 'wind_dir', 'wind_str']].round().astype(int)

    # Speichern der Durchschnittswerte in einer neuen CSV-Datei
    data.index = data.index.astype(str)
    data.to_csv(trendFileFormat.format(station['name']), sep=";", index=True)