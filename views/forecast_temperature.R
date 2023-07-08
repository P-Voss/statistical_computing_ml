
library('dplyr')
library('ggplot2')

source("views/functions/singleSourceAggregations.R")
source("views/functions/singleSourcePlots.R")

files <- list.files(path="data/trend/temperature/", pattern="*.csv", full.names=TRUE, recursive=FALSE)

lapply(files, function (file) {
    dataset <- read.csv(file, sep=";", head=TRUE)
    dataset$datehour <- as.POSIXct(strptime(dataset$datehour, format="%Y%m%d%H"))

    values <- transformToAvgValues(dataset)

    plot <- exactDiagram(file, values, -10, 30, 1, "Monat in 2023", "Temperatur (Grad Celsius)")

    # Fügt dem Plot eine Extra-Linie zur Hervorhebung der 0 Grad hinzu
    plot <- plot +
        geom_hline(yintercept = 0, linetype = "solid", color = "lightblue", size = 0.5)

})

