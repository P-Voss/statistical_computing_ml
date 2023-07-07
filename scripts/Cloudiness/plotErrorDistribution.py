import numpy
import matplotlib.pyplot as plot
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
plotFileFormat = "../../data/plots/cloudiness/{}_error_distribution.png"

for station in stations:
    errors = numpy.load(errorsFileFormat.format(station['name']))

    stats.probplot(errors, dist="norm", plot=plot)
    plot.savefig(plotFileFormat.format(station['name']))
    plot.close()

print('Done')