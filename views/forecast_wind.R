
library('dplyr')
library('ggplot2')

source("views/functions/singleSourceAggregations.R")
source("views/functions/singleSourcePlots.R")

files <- list.files(path="data/trend/wind/", pattern="*.csv", full.names=TRUE, recursive=FALSE)

lapply(files, function (file) {
    dataset <- read.csv(file, sep=";", head=TRUE)
    dataset$datehour <- as.POSIXct(strptime(dataset$datehour, format="%Y%m%d%H"))

    values <- transformToAvgValues(dataset)

    plot <- exactDiagram(file, values, 0, 12, 1, "Monat in 2023", "Windstärke (Bft)")

})

