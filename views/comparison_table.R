
# Bibliothek zur Darstellung von (schönen) Tabellen
library(knitr)

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

sortedScores <- scores[order(scores$score),]

kable(sortedScores[1:25, ])
