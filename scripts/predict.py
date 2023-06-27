import pandas
import numpy
from datetime import date, timedelta
import tensorflow.python.keras.models
import joblib


def daterange(startDate, endDate):
    for n in range(int((endDate - startDate).days)):
        yield startDate + timedelta(n)

def getSeason(month):
    if month == 1 or month == 2 or month == 12:
        return 4
    if month == 3 or month == 4 or month == 5:
        return 1
    if month == 6 or month == 7 or month == 8:
        return 2
    return 3



trendFileFormat = '../data/trend/{}.csv'
modelFileFormat = 'Temperature/training/{}/model.h5'
scalerFileFormat = 'Temperature/training/{}/scaler.pkl'
predictionFileFormat = '../data/trend/{}_prediction.csv'

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

startDate = date(2023, 1, 1)
endDate = date(2023, 12, 31)


for station in stations:

    model = tensorflow.keras.models.load_model(modelFileFormat.format(station['name']))
    scaler = joblib.load(scalerFileFormat.format(station['name']))

    df = pandas.read_csv(trendFileFormat.format(station['name']), delimiter=";", dtype={'date': str})
    df.set_index('date', inplace=True)
    df.index = df.index.astype(str)

    data = []
    for single_date in daterange(startDate, endDate):
        season = getSeason(single_date.month)
        for single_hour in range(24):
            key = single_date.strftime("%m%d") + str(single_hour).rjust(2, "0")
            if key not in df.index:
                continue
            else:
                row = df.loc[key].copy()

                row['season_1'] = 1 if season == '1' else 0
                row['season_2'] = 1 if season == '2' else 0
                row['season_3'] = 1 if season == '3' else 0
                row['season_4'] = 1 if season == '4' else 0
                row['year'] = 2023
                row['month'] = single_date.month
                row['day'] = single_date.day
                row['hour_sin'] = numpy.sin(2 * numpy.pi * single_hour / 24)
                row['hour_cos'] = numpy.cos(2 * numpy.pi * single_hour / 24)

                features = row[
                    ['season_1', 'season_2', 'season_3', 'season_4', 'year', 'month', 'day', 'hour_sin', 'hour_cos',
                     'prev_temp', 'prev_hum', 'humidity', 'coverage', 'wind_dir', 'wind_str', 'prec']]

                # Skalieren Sie Ihre Vorhersagedaten
                features = scaler.transform([features])

                features_reshaped = numpy.expand_dims(features, axis=0)

                prediction = model.predict(features_reshaped)
                data.append({'date': single_date.strftime('%Y-%m-%d'), 'hour': single_hour, 'prediction': prediction[0][0]})
    df_predictions = pandas.DataFrame(data)
    df_predictions.to_csv(predictionFileFormat.format(station['name']), index=False, sep=';')

