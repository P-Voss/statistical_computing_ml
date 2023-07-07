import pandas
import numpy
import json
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

# Bewölkungsgrad liegt zwischen 0 und 8
def normalizeValue(value):
    return min(
        8,
        max(
            0,
            value
        )
    )


trendFileFormat = '../data/trend/{}.csv'
modelFileFormat = 'Cloudiness/training/{}/model.h5'
scalerFileFormat = 'Cloudiness/training/{}/scaler.pkl'
predictionFileFormat = '../data/trend/cloudiness/{}_prediction.csv'
reportFilePath = 'Cloudiness/training/cloudiness_report.json'

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

startDate = date(2023, 1, 1)
endDate = date(2023, 12, 31)
with open(reportFilePath) as file:
    report = json.load(file)

for station in stations:

    mae = report[station['name']]['mae']
    stdDev = report[station['name']]['stdDev']
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
                     'prev_temp', 'prev_hum', 'humidity', 'temp', 'wind_dir', 'wind_str', 'prec']]
                features = pandas.DataFrame([features], columns=[
                    'season_1', 'season_2', 'season_3', 'season_4', 'year', 'month', 'day', 'hour_sin', 'hour_cos',
                    'prev_temp', 'prev_hum', 'humidity', 'temp', 'wind_dir', 'wind_str', 'prec'
                ])
                # Skalieren Sie Ihre Vorhersagedaten
                features = scaler.transform(features)

                features_reshaped = numpy.expand_dims(features, axis=0)

                prediction = model.predict(features_reshaped)
                upperConfidence = prediction[0][0] + 1.645 * stdDev
                lowerConfidence = prediction[0][0] - 1.645 * stdDev

                data.append(
                    {
                        'datehour': single_date.strftime('%Y%m%d') + str(single_hour).rjust(2, '0'),
                        'date': single_date.strftime('%Y-%m-%d'),
                        'hour': single_hour,
                        'prediction': normalizeValue(prediction[0][0]),
                        'upper_bound_mae': normalizeValue(prediction[0][0] + mae),
                        'lower_bound_mae': normalizeValue(prediction[0][0] - mae),
                        'upper_bound_confidence_90': normalizeValue(upperConfidence),
                        'lower_bound_confidence_90': normalizeValue(lowerConfidence),
                        'trend': normalizeValue(row['coverage'])
                    }
                )
    df_predictions = pandas.DataFrame(data)
    df_predictions.to_csv(predictionFileFormat.format(station['name']), index=False, sep=';')

