
library('dplyr')
library('ggplot2')


transformToAvgValues <- function(data) {
    avg_values <- data %>%
        group_by(date, station) %>%
        summarise_all(mean, na.rm = TRUE)
    avg_values$date <- as.Date(avg_values$date)
    return(avg_values)
}

readStation <- function (filepath, stationName) {
    data <- read.csv(filepath, sep = ";")
    data$datehour <- as.POSIXct(strptime(data$MESS_DATUM, format="%Y%m%d%H"))
    data$station <- stationName
    data <- data %>%
        filter(datehour >= as.POSIXct("2020-01-01") & datehour <= as.POSIXct("2022-12-31"))
}

arkona <- readStation("data/history/Arkona.csv", "Arkona")
boltenhagen <- readStation("data/history/Boltenhagen.csv", "Boltenhagen")
cuxhaven <- readStation("data/history/Cuxhaven.csv", "Cuxhaven")
emden <- readStation("data/history/Emden.csv", "Emden")
fehmarn <- readStation("data/history/Fehmarn.csv", "Fehmarn")
hattstedt <- readStation("data/history/Hattstedt.csv", "Hattstedt")
hohwacht <- readStation("data/history/Hohwacht.csv", "Hohwacht")
karlshagen <- readStation("data/history/Karlshagen.csv", "Karlshagen")
konstanz <- readStation("data/history/Konstanz.csv", "Konstanz")
ueckermuende <- readStation("data/history/Ueckermuende.csv", "Ueckermuende")


gatheredData <- data.frame()
gatheredData <- rbind(arkona, boltenhagen, cuxhaven, emden, fehmarn, hattstedt, hohwacht, karlshagen, konstanz, ueckermuende)
gatheredData$date <- as.Date(gatheredData$datehour)
gatheredData <- transformToAvgValues(gatheredData)

ggplot(gatheredData, aes(x = datehour, y = TT_TER, color = station)) +
    ggtitle("Temperaturen pro Station") +
    geom_line() +
    # geom_smooth() +
    # geom_point() +
    facet_wrap(~station) +
    coord_cartesian(ylim = c(-10, 35)) +
    scale_y_continuous(breaks = seq(-10, 35, 1)) +
    labs(x = "Zeit", y = "Temperatur", color = "Wetterstation") +
    theme_bw()

ggplot(gatheredData, aes(x = datehour, y = N_TER, color = station)) +
    ggtitle("Bedeckung pro Station") +
    geom_line() +
    # geom_smooth(se = FALSE) +
    # geom_point() +
    facet_wrap(~station) +
    coord_cartesian(ylim = c(0, 8)) +
    scale_y_continuous(breaks = seq(0, 8, 1)) +
    labs(x = "Zeit", y = "Bedeckungsgrad", color = "Wetterstation") +
    theme_bw()

ggplot(gatheredData, aes(x = datehour, y = FK_TER, color = station)) +
    ggtitle("Windgeschwindigkeiten pro Station") +
    geom_line() +
    # geom_smooth() +
    # geom_point() +
    facet_wrap(~station) +
    coord_cartesian(ylim = c(0, 12)) +
    scale_y_continuous(breaks = seq(0, 12, 1)) +
    labs(x = "Zeit", y = "Windgeschwindigkeit in Bft", color = "Wetterstation") +
    theme_bw()



ggplot(gatheredData, aes(x = datehour, y = TT_TER, color = station)) +
    ggtitle("Temperaturen aller Stationen") +
    # geom_line(alpha = 0.6) +
    geom_smooth(se = FALSE, span=0.8) +
    # geom_point() +
    coord_cartesian(ylim = c(-10, 35)) +
    scale_y_continuous(breaks = seq(-10, 35, 1)) +
    labs(x = "Zeit", y = "Temperatur", color = "Wetterstation") +
    theme_bw()

ggplot(gatheredData, aes(x = datehour, y = N_TER, color = station)) +
    ggtitle("Bedeckungsgrade aller Stationen") +
    # geom_line(alpha = 0.6) +
    geom_smooth(se = FALSE, span=0.8) +
    # geom_point() +
    coord_cartesian(ylim = c(0, 8)) +
    scale_y_continuous(breaks = seq(0, 8, 1)) +
    labs(x = "Zeit", y = "Bedeckungsgrad", color = "Wetterstation") +
    theme_bw()

ggplot(gatheredData, aes(x = datehour, y = FK_TER, color = station)) +
    ggtitle("Windgeschwindigkeiten aller Stationen") +
    # geom_line(alpha = 0.6) +
    geom_smooth(se = FALSE, span=0.8) +
    # geom_point() +
    coord_cartesian(ylim = c(0, 12)) +
    scale_y_continuous(breaks = seq(0, 12, 1)) +
    labs(x = "Zeit", y = "Windgeschwindigkeit in Bft", color = "Wetterstation") +
    theme_bw()
