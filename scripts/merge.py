
import pandas
import numpy

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
    {'name': 'Ueckermuende'},
]

cloudinessFileFormat = '../data/source/Cloudiness/{}/product.txt'
rangeFileFormat = '../data/source/Range/{}/product.txt'
temperatureFileFormat = '../data/source/Temperature/{}/product.txt'
windFileFormat = '../data/source/Wind/{}/product.txt'

trainingFileFormat = '../data/training/{}_filtered.csv'
mergedFileFormat = '../data/history/{}.csv'

for station in stations:

    # N_TER = Terminwert Bedeckungsgrad (in Achtel 0-9)
    cloudinessDf = pandas.read_csv(cloudinessFileFormat.format(station['name']), delimiter=';', usecols=['MESS_DATUM', 'N_TER'])

    # VK_TER = Terminwert Sichtweite
    rangeDf = pandas.read_csv(rangeFileFormat.format(station['name']), delimiter=';', usecols=['MESS_DATUM', 'VK_TER'])

    # TT_TER = Terminwert Lufttemperatur
    # RF_TER = Terminwert relative Feuchte
    temperatureDf = pandas.read_csv(temperatureFileFormat.format(station['name']), delimiter=';', usecols=['MESS_DATUM', 'TT_TER', 'RF_TER'])

    # DK_TER = Terminwert Windrichtung (32-teilig in Grad)
    # FK_TER = Terminwert Windstärke
    windDf = pandas.read_csv(windFileFormat.format(station['name']), delimiter=';', usecols=['MESS_DATUM', 'DK_TER', 'FK_TER'])

    mergedData = pandas.merge(cloudinessDf, rangeDf, on='MESS_DATUM', how='outer')
    mergedData = pandas.merge(mergedData, temperatureDf, on='MESS_DATUM', how='outer')
    mergedData = pandas.merge(mergedData, windDf, on='MESS_DATUM', how='outer')

    mergedData.replace(-999, numpy.nan, inplace=True)

    mergedData.to_csv(mergedFileFormat.format(station['name']), sep=';', index=False)

    filteredData = mergedData.dropna()
    filteredData.to_csv(trainingFileFormat.format(station['name']), sep=';', index=False)
