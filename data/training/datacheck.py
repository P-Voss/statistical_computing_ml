
import pandas

file = pandas.read_csv("Arkona_training.csv", sep = ";")

print(file.describe())
