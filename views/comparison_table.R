
# Bibliothek zur Darstellung von (schönen) Tabellen
library(knitr)
library(tidyr)

source("views/functions/scoring.R")

arkona <- loadScores("Arkona")
boltenhagen <- loadScores("Boltenhagen")
cuxhaven <- loadScores("Cuxhaven")
emden <- loadScores("Emden")
fehmarn <- loadScores("Fehmarn")
hattstedt <- loadScores("Hattstedt")
hohwacht <- loadScores("Hohwacht")
karlshagen <- loadScores("Karlshagen")
konstanz <- loadScores("Konstanz")
ueckermuende <- loadScores("Ueckermuende")

scores <- rbind(
    arkona,
    boltenhagen,
    cuxhaven,
    emden,
    fehmarn,
    hattstedt,
    hohwacht,
    karlshagen,
    konstanz,
    ueckermuende
)
scores <- drop_na(scores)

sortedScores <- scores[order(scores$Gesamt),]

kable(sortedScores[1:25, 1:7])
