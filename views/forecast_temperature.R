
library('dplyr')
library('ggplot2')

files <- list.files(path="data/trend/temperature/", pattern="*.csv", full.names=TRUE, recursive=FALSE)

smoothDiagram <- function (file, data) {
    ggplot(data, aes(x = data$date)) +
        ggtitle(file) +
        geom_ribbon(aes(ymin = data$lower_bound_mae, ymax = data$upper_bound_mae, fill = "Mittlerer Schätzungsfehler"), alpha = 0.2) +
        geom_ribbon(aes(ymin = data$lower_bound_confidence_90, ymax = data$upper_bound_confidence_90, fill = "90% Confidence"), alpha = 0.2) +
        geom_smooth(aes(y = data$prediction, colour = "Vorhersage"), method = "loess", span=0.4) +
        geom_smooth(aes(y = data$trend, colour = "Typischer Wert"), method = "loess", span=0.4) +
        scale_fill_manual(values = c("Mittlerer Schätzungsfehler" = "blue", "90% Confidence" = "orange"),
                        name = "Legend") +
        scale_color_manual(values = c("Vorhersage" = "blue", "Typischer Wert" = "red"),
                name = "Legend") +
        scale_x_date(date_breaks = "1 month", date_labels = "%b") +
        xlab("Monat in 2023") +
        ylab("Temperatur in Grad Celsius") +
        theme_bw() +
        theme(plot.title = element_text(size = 20, face = "bold"),
            axis.title = element_text(size = 12),
            axis.text.x = element_text(size = 10))
}

scatterPlot <- function (file, data) {
    ggplot(data, aes(x = data$date, y = data$prediction)) +
        ggtitle(file) +
        scale_x_date(date_breaks = "1 month", date_labels = "%b") +
        geom_point(color = "blue")
}


exactDiagram <- function (file, data) {
    ggplot(data, aes(x= data$date)) +
        ggtitle(file) +
        geom_ribbon(aes(ymin = data$lower_bound_mae, ymax = data$upper_bound_mae, , fill = "MAE"), alpha = 0.2) +
        geom_ribbon(aes(ymin = data$lower_bound_confidence_90, ymax = data$upper_bound_confidence_90, fill = "90% Confidence"), alpha = 0.2) +
        geom_line(aes(y = data$prediction, colour = "Vorhersage")) +
        geom_line(aes(y = data$trend, colour = "Typischer Wert")) +
        scale_fill_manual(values = c("MAE" = "blue", "90% Confidence" = "orange"),
                        name = "Schwankungsbereiche") +
        scale_color_manual(values = c("Vorhersage" = "blue", "Typischer Wert" = "red"),
                name = "Vorhersagen") +
        scale_x_date(date_breaks = "1 month", date_labels = "%b") +
        xlab("Monat in 2023") +
        ylab("Temperatur in Grad Celsius") +
        theme_bw() +
        theme(plot.title = element_text(size = 20, face = "bold"),
            axis.title = element_text(size = 12),
            axis.text.x = element_text(size = 10))
}


lapply(files, function (file) {
    dataset <- read.csv(file, sep=";", head=TRUE)
    dataset$datehour <- as.POSIXct(strptime(dataset$datehour, format="%Y%m%d%H"))
    max_values <- dataset %>%
      group_by(date) %>%
      summarise_all(max, na.rm = TRUE)
    max_values$date <- as.Date(max_values$date)

    exactDiagram(file, max_values)
    # smoothDiagram(file, max_values)
    # scatterPlot(file, max_values)

    # head(max_values, 5)
})

