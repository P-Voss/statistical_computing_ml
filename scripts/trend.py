from sklearn.linear_model import LinearRegression
from datetime import datetime, timedelta
import calendar
import pandas as pd
import numpy as np

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
    {'name': 'Ploen'},
    {'name': 'Prien'},
    {'name': 'Ueckermuende'},
]

for station in stations:
    df = pd.read_csv(importFileFormat.format(station['name']), delimiter=";")

    # Datumsspalte in ein datetime-Objekt umwandeln und den Tag und die Stunde extrahieren
    date = pd.to_datetime(df['MESS_DATUM'], format='%Y%m%d%H')
    df['date'] = date.dt.strftime('%m%d%H')

    # Durchschnitt pro Tag und Stunde berechnen
    data = df.groupby('date').mean()
    # Entferne Daten die später abgeleitet werden können
    data = data.drop(columns=['hour_sin', 'hour_cos', 'season', 'year', 'month', 'day', 'hour', 'coverage_class', 'MESS_DATUM'])

    # Werte runden
    data[['coverage', 'wind_dir', 'wind_str']] = data[['coverage', 'wind_dir', 'wind_str']].round().astype(int)

    # Speichern der Durchschnittswerte in einer neuen CSV-Datei
    data.index = data.index.astype(str)
    data.to_csv(trendFileFormat.format(station['name']), sep=";", index=True)