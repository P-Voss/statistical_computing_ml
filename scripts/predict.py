import pandas
from datetime import date, timedelta


def daterange(startDate, endDate):
    for n in range(int((endDate - startDate).days)):
        yield startDate + timedelta(n)

trendFileFormat = '../data/trend/{}.csv'

stations = [
    {'name': 'Arkona'},
    # {'name': 'Boltenhagen'},
    # {'name': 'Cuxhaven'},
    # {'name': 'Emden'},
    # {'name': 'Fehmarn'},
    # {'name': 'Hattstedt'},
    # {'name': 'Hohwacht'},
    # {'name': 'Karlshagen'},
    # {'name': 'Konstanz'},
    # {'name': 'Ploen'},
    # {'name': 'Prien'},
    # {'name': 'Ueckermuende'},
]

startDate = date(2023, 1, 1)
endDate = date(2023, 12, 31)


for station in stations:

    df = pandas.read_csv(trendFileFormat.format(station['name']), delimiter=";", dtype={'date': str})
    df.set_index('date', inplace=True)
    df.index = df.index.astype(str)

    for single_date in daterange(startDate, endDate):
        for hour in range(23):
            key = single_date.strftime("%m%d") + str(hour).rjust(2, "0")
            if key not in df.index:
                continue
            else:
                row = df.loc[key]
                print(row)


