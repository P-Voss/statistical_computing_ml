
# Alternative zur Trendbildung per arithm. Mittel
# Nutzt lineare Regression zur Generierung der Wetterdaten anhand historischer Daten
# (Wird für die Fallstudie nicht genutzt)

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
    {'name': 'Ueckermuende'},
]

for station in stations:
    df = pd.read_csv(importFileFormat.format(station['name']), delimiter=";")

    mask = (df['year'] >= 1955) & (df['year'] <= 2022)
    df = df.loc[mask]

    features = ['prev_temp', 'prev_hum', 'temp', 'humidity', 'coverage_class', 'coverage', 'range', 'wind_dir', 'wind_str', 'prec']

    results = []
    for month in range(1, 13):
        for day in range(1, 32):
            if month == 2 and day > 28:
                continue
            if day > 30 and (month in [4, 6, 9, 11]):
                continue
            for hour in range(24):
                subset = df[(df['month'] == month) & (df['day'] == day) & (df['hour'] == hour)]
                if len(subset) < 2:
                    continue
                for year in range(2023, 2026):
                    row = [datetime(year, month, day, hour)]
                    for feature in features:
                        model = LinearRegression()
                        model.fit(subset['year'].values.reshape(-1, 1), subset[feature])
                        temp_pred = model.predict(np.array([[year]]))
                        row.append(temp_pred[0])
                    # Fügen Sie die "row"-Liste zur "results"-Liste hinzu
                    results.append(row)

    columns = ['MESS_DATUM'] + features
    df_pred = pd.DataFrame(results, columns=columns)
    df_pred.to_csv(trendFileFormat.format(station['name']), index=False, sep=';')