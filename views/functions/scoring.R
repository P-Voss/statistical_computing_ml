
# Bibliothek für gleitende Varianz - rollapply
library('zoo')

source("views/functions/singleSourceAggregations.R")


# private Funktion, nur für Aufrufe innerhalb dieser Datei vorgesehen
.readFile <- function(filepath) {
    data <- read.csv(filepath, sep = ";", stringsAsFactors = FALSE)
    data$date <- as.Date(data$date, format="%Y-%m-%d")
    data <- transformToAvgValues(data)
    return(data)
}

# private Funktion, nur für Aufrufe innerhalb dieser Datei vorgesehen
.transformToRollingScore <- function(data) {
    date_values <- data$date
    prediction_values <- data$prediction

    # maxValue <- max(prediction_values)
    # minValue <- min(prediction_values)
    # mean <- mean(prediction_values)

    # Ermittelt gleitenden Variationskoeffizient über 14-Tages-Intervalle
    # (nicht ändern - oder auch Scorenormalisierung ändern)
    relStdDev <- rollapply(prediction_values, width = 14, FUN = function(x) {
        sd(x, na.rm = TRUE) / mean(x, na.rm = TRUE)
    }, fill = NA, align = "right")

    # Normalisiert Lagemaß um Score zu ermitteln (nach Bedarf ändern)
    score <- .normalizeRelative(relStdDev)

    # Teilt die Tagesdaten in 14-Tages-Intervalle auf, werden den Scores zugeordnet
    # (nicht ändern)
    date_frame <- rollapply(date_values, width = 14, FUN = function(x) {
        c(startDate = as.Date(head(x, 1)),
          endDate = as.Date(tail(x, 1)))
    }, by.column = FALSE, fill = NA, align = "right")

    date_frame_df <- data.frame(date_frame)

    result <- data.frame(
        score = score,
        startDate = date_frame_df$startDate,
        endDate = date_frame_df$endDate
    )

    result$startDate <- as.Date(result$startDate, origin = "1970-01-01")
    result$endDate <- as.Date(result$endDate, origin = "1970-01-01")

    return(result)
}

# private Funktion, nur für Aufrufe innerhalb dieser Datei vorgesehen
# normalisiert die Varianzen, um Gewichtung insb. für Temperatur aufzulösen
# Faktor 10, um für die spätere Anzeige einen höheren Score zwischen 0 und 10 zu erhalten (je Wetteraspekt)
# @todo Normalisiert aktuell auf Basis des 14-Tage Sets, Gesamtset macht wahrscheinlich mehr Sinn?
.normalizeVariance <- function(variance) {
    return (
        10 * ((variance - min(variance, na.rm = TRUE)) / (max(variance, na.rm = TRUE) - min(variance, na.rm = TRUE)))
    )
}

# private Funktion, nur für Aufrufe innerhalb dieser Datei vorgesehen
# normalisiert die Standardabweichung in Relation zu Höchst- und Mindestwerten des Datensets
# Faktor 10, um für die spätere Anzeige einen höheren Score zwischen 0 und 10 zu erhalten (je Wetteraspekt)
.normalizeMinMaxTotal <- function(value, min, max) {
    return (
        10 * ((value - min) / (max - min))
    )
}

# private Funktion, nur für Aufrufe innerhalb dieser Datei vorgesehen
# normalisiert die relative Standardabweichung gegen Höchstwerte der relativen Standardabweichungen
# Faktor 10, um für die spätere Anzeige einen höheren Score zwischen 0 und 10 zu erhalten (je Wetteraspekt)
.normalizeRelative <- function(relStdDev) {
    return (
        10 * ((relStdDev - min(relStdDev, na.rm = TRUE)) /
        (max(relStdDev, na.rm = TRUE) - min(relStdDev, na.rm = TRUE)))
    )
}

# private Funktion, nur für Aufrufe innerhalb dieser Datei vorgesehen
# Standardisiert die Varianzen, um Gewichtung auf Temperatur aufzulösen
.standardize <- function(x) {
    return((x - mean(x, na.rm = TRUE)) / sd(x, na.rm = TRUE))
}


loadScores <- function (stationName) {
    cloudinessFilename <- paste0("data/trend/cloudiness/", stationName, "_prediction.csv")
    cloudinessDf <- .readFile(cloudinessFilename)
    cloudinessVar <- .transformToRollingScore(cloudinessDf)

    windFilename <- paste0("data/trend/wind/", stationName, "_prediction.csv")
    windDf <- .readFile(windFilename)
    windVar <- .transformToRollingScore(windDf)

    tempFilename <- paste0("data/trend/temperature/", stationName, "_prediction.csv")
    tempDf <- .readFile(tempFilename)
    tempVar <- .transformToRollingScore(tempDf)

    # hier Bezeichnungen für spätere Labels vergeben
    scores <- data.frame(
        begin = cloudinessVar$startDate,
        end = cloudinessVar$endDate,
        Bedeckung = cloudinessVar$score,
        Windgeschwindigkeit = windVar$score,
        Temperatur = tempVar$score,
        Gesamt = cloudinessVar$score + windVar$score + tempVar$score,
        station = stationName
    )

    return(scores)
}