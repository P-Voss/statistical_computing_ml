import json
import numpy
import scipy.stats as stats

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

errorsFileFormat = "training/{}/errors.npy"
plotFileFormat = "../../data/plots/{}_error_distribution.png"

for station in stations:
    errors = numpy.load(errorsFileFormat.format(station['name']))

    # Daten standardisieren
    standardized_data = (errors - numpy.mean(errors)) / numpy.std(errors)

    # Durchführen des Kolmogorov-Smirnov-Tests
    ks_statistic, p_value = stats.kstest(standardized_data, 'norm')

    print('Statistik für: ' + station['name'])
    print('KS statistic:', ks_statistic)
    print('p-value:', p_value)
