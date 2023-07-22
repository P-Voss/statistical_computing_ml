
source("views/functions/singleSourceAggregations.R")
source("views/functions/singleSourcePlots.R")

files <- list.files(path="data/trend/wind/", pattern="*.csv", full.names=TRUE, recursive=FALSE)

lapply(files, function (file) {
    dataset <- read.csv(file, sep=";", head=TRUE)
    dataset$datehour <- as.POSIXct(strptime(dataset$datehour, format="%Y%m%d%H"))
    values <- transformToAvgValues(dataset)
    # values <- transformToMaxValues(dataset)

    plot <- exactDiagram(file, values, 0, 36, 3, "Monate (2023)", "Windgeschwindigkeit in m/s")
})

