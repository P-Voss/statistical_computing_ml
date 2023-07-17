
library('tidyr')
# Bibliothek zur Arbeit mit Datum und Uhrzeit
library('lubridate')
library('dplyr')
library('ggplot2')
library('plotly')

source("views/functions/singleSourceAggregations.R")
source("views/functions/scoring.R")


# private Funktion, nur für Aufrufe innerhalb dieser Datei vorgesehen
.readFile <- function(filepath) {
    data <- read.csv(filepath, sep = ";")
    data <- transformToAvgValues(data)

    return(data)
}

# private Funktion, nur für Aufrufe innerhalb dieser Datei vorgesehen
.readStation <- function (stationName) {
    cloudinessFilename <- paste0("data/trend/cloudiness/", stationName, "_prediction.csv")
    cloudinessDf <- .readFile(cloudinessFilename)

    windFilename <- paste0("data/trend/wind/", stationName, "_prediction.csv")
    windDf <- .readFile(windFilename)

    tempFilename <- paste0("data/trend/temperature/", stationName, "_prediction.csv")
    tempDf <- .readFile(tempFilename)

    stationData <- data.frame(
        date = cloudinessDf$date,
        Bedeckungsgrad = cloudinessDf$prediction,
        Windgeschwindigkeit = windDf$prediction,
        Temperatur = tempDf$prediction,
        station = stationName
    )

    return(stationData)
}

.pivotData <- function (dataframe) {
    pivot <- dataframe %>%
        pivot_longer(
            cols = c(Bedeckungsgrad, Windgeschwindigkeit, Temperatur),
            names_to = "variable",
            values_to = "value"
        )
    return(pivot)
}



generatePlot <- function (stationName) {
    data <- .readStation(stationName)
    scores <- loadScores(stationName)
    min_score_interval <- scores[which.min(scores$score), c("begin", "end")]

    pivottedData <- .pivotData(data)

    label <- paste("Vorhersage: Wetter in", stationName, "2023")

    plot <- ggplot(data = pivottedData, aes(x = date, y = value, colour = variable)) +
        geom_line() +

        coord_cartesian(ylim = c(-5, 30)) +
        scale_y_continuous(breaks = seq(-5, 30, 1)) +

        # vertikale Linien an den Anfang und das Ende des Intervalls mit dem niedrigsten Score zeichnen
        # todo (?): geom_rect() wäre evtl schöner; entsprechende min- und max- Werter für Höhe der Box erfassen
        geom_vline(aes(xintercept = as.numeric(min_score_interval$begin)), linetype = "dashed", color = "red", linewidth = 1.0) +
        geom_vline(aes(xintercept = as.numeric(min_score_interval$end)), linetype = "dashed", color = "red", linewidth = 1.0) +

        # horizontale Linie zur Kennzeichnung des 0-Wertes
        geom_hline(yintercept = 0, linetype = "solid", color = "lightblue", size = 0.5) +

        scale_x_date(date_breaks = "1 month", date_labels = "%b") +
        labs(title = label, x = "Date", y = "Value", colour = "Wetterfaktoren") +
        theme_bw() +
        theme(plot.title = element_text(size = 20, face = "bold"),
            axis.title = element_text(size = 12),
            axis.text.x = element_text(size = 10)
        )
    return(plot)
}


# Diagramm per Plotly generieren? Erlaubt eine zweite Skala für bft. oder Bedeckungsgrad
# generatePlotly <- function (stationName) {
#     data <- .readStation(stationName)
#     scores <- loadScores(stationName)
#     min_score_interval <- scores[which.min(scores$score), c("begin", "end")]
#
#     pivottedData <- .pivotData(data)
#
#
#     p <- plot_ly()
#
#     for (variable in unique(pivottedData$variable)) {
#         if (variable == "Temperatur") {
#             p <- add_trace(p, data = pivottedData[pivottedData$variable == variable, ],
#                             x = ~date, y = ~value, type = 'scatter', mode = 'lines',
#                             line = list(color = 'red'), name = variable, yaxis = 'y1')
#         } else {
#             p <- add_trace(p, data = pivottedData[pivottedData$variable == variable, ],
#                             x = ~date, y = ~value, type = 'scatter', mode = 'lines',
#                             line = list(color = ifelse(variable == "Bedeckungsgrad", 'blue', 'green')),
#                             name = variable, yaxis = 'y2')
#         }
#     }
#
#     p <- layout(p, title = paste("Vorhersage: Wetter in", stationName, "2023"),
#                 yaxis = list(title = 'Temperatur'),
#                 yaxis2 = list(title = 'Bedeckungsgrad / Windgeschwindigkeit', overlaying = 'y', side = 'right'))
#
#     return(p)
# }
