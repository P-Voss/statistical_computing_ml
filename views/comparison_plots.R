
library('dplyr')
# Bibliothek zum Formatieren von DataFrames - Pivot
library('tidyr')
library('ggplot2')

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

lowestScores <- rbind(
    arkona = arkona[which.min(arkona$Gesamt), ],
    boltenhagen = boltenhagen[which.min(boltenhagen$Gesamt), ],
    cuxhaven = cuxhaven[which.min(cuxhaven$Gesamt), ],
    emden = emden[which.min(emden$Gesamt), ],
    fehmarn = fehmarn[which.min(fehmarn$Gesamt), ],
    hattstedt = hattstedt[which.min(hattstedt$Gesamt), ],
    hohwacht = hohwacht[which.min(hohwacht$Gesamt), ],
    karlshagen = karlshagen[which.min(karlshagen$Gesamt), ],
    konstanz = konstanz[which.min(konstanz$Gesamt), ],
    ueckermuende = ueckermuende[which.min(ueckermuende$Gesamt), ]
)

# print(lowestScores)

# Daten von Spalten in Zeilen pivotieren, damit sie im Diagramm dargestellt werden können
lowestScoresPlot <- lowestScores %>%
    tidyr::pivot_longer(cols = c(Windgeschwindigkeit, Bedeckung, Temperatur, Gesamt),
                      names_to = "Variable",
                      values_to = "Value")

# Label für das Diagramm
lowestScoresPlot$label <- paste(
    lowestScoresPlot$station,
    paste(
        format(lowestScoresPlot$begin, "%d.%m.%Y"),
        format(lowestScoresPlot$end, "%d.%m.%Y"),
        sep = " - "
    ),
    sep = "\n")

# Plot
ggplot(lowestScoresPlot, aes(x = reorder(label, Value), y = Value, fill = Variable)) +
    geom_bar(stat = "identity", position = "dodge") +
    theme_bw() +
    xlab("Wetterstation und Zeitraum") +
    ylab("Variabilitaet") +
    labs(fill = "Variabilitaetsscores") +
    theme(axis.text.x = element_text(angle = 45, hjust = 1)) +
    ggtitle("geringste 2-woechige Variabilitaet in 2023 je Wetterstation")
