
library('dplyr')
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
    arkona = arkona[which.min(arkona$score), ],
    boltenhagen = boltenhagen[which.min(boltenhagen$score), ],
    cuxhaven = cuxhaven[which.min(cuxhaven$score), ],
    emden = emden[which.min(emden$score), ],
    fehmarn = fehmarn[which.min(fehmarn$score), ],
    hattstedt = hattstedt[which.min(hattstedt$score), ],
    hohwacht = hohwacht[which.min(hohwacht$score), ],
    karlshagen = karlshagen[which.min(karlshagen$score), ],
    konstanz = konstanz[which.min(konstanz$score), ],
    ueckermuende = ueckermuende[which.min(ueckermuende$score), ]
)

# print(lowestScores)

# Daten von Spalten in Zeilen pivotieren, damit sie im Diagramm dargestellt werden können
lowestScoresPlot <- lowestScores %>%
    tidyr::pivot_longer(cols = c(wind_var, cloudiness_var, temp_var, score),
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
    theme_minimal() +
    xlab("Wetterstation") +
    ylab("Variabilitaet") +
    theme(axis.text.x = element_text(angle = 45, hjust = 1)) +
    ggtitle("geringste 2-woechige Variabilitaet in 2023 je Wetterstation")
