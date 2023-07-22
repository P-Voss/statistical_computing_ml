
library('dplyr')
library('ggplot2')
library('stringr')

getTitle <- function (filepath) {
    location <- regexpr("(\\w*)_prediction.csv", filepath)
    title <- substr(filepath, location, location+attr(location, "match.length") - 1)
    return(str_remove(title, "_prediction.csv"))
}

smoothDiagram <- function (file, data, lowerLimit, upperLimit, steps, xlab, ylab) {
    plot <- ggplot(data, aes(x = data$date)) +
        ggtitle(getTitle(file)) +
        coord_cartesian(ylim = c(lowerLimit, upperLimit)) +
        scale_y_continuous(breaks = seq(lowerLimit, upperLimit, steps)) +
        geom_ribbon(aes(ymin = data$lower_bound_mae, ymax = data$upper_bound_mae, fill = "Mittlerer Schätzungsfehler"), alpha = 0.2) +
        geom_ribbon(aes(ymin = data$lower_bound_confidence_90, ymax = data$upper_bound_confidence_90, fill = "90% Confidence"), alpha = 0.2) +
        geom_smooth(aes(y = data$prediction, colour = "Vorhersage"), method = "loess", span=0.4) +
        geom_smooth(aes(y = data$trend, colour = "Typischer Wert"), method = "loess", span=0.4) +
        scale_fill_manual(values = c("MAE" = "blue", "90% Confidence" = "orange"),
                        name = "Schwankungsbereiche") +
        scale_color_manual(values = c("Vorhersage" = "blue", "Typischer Wert" = "red"),
                name = "Legend") +
        scale_x_date(date_breaks = "1 month", date_labels = "%b") +
        xlab(xlab) +
        ylab(ylab) +
        theme_bw() +
        theme(plot.title = element_text(size = 20, face = "bold"),
            axis.title = element_text(size = 12),
            axis.text.x = element_text(size = 10))

    return(plot)
}

scatterPlot <- function (file, data) {
    plot <- ggplot(data, aes(x = data$date, y = data$prediction)) +
        ggtitle(getTitle(file)) +
        scale_x_date(date_breaks = "1 month", date_labels = "%b") +
        geom_point(color = "blue")

    return(plot)
}

exactDiagram <- function (file, data, lowerLimit, upperLimit, steps, xlab, ylab) {
    plot <- ggplot(data, aes(x = data$date)) +
        ggtitle(getTitle(file)) +
        coord_cartesian(ylim = c(lowerLimit, upperLimit)) +
        scale_y_continuous(breaks = seq(lowerLimit, upperLimit, steps)) +
        geom_ribbon(aes(ymin = data$lower_bound_mae, ymax = data$upper_bound_mae, , fill = "MAE"), alpha = 0.2) +
        geom_ribbon(aes(ymin = data$lower_bound_confidence_90, ymax = data$upper_bound_confidence_90, fill = "90% Confidence"), alpha = 0.2) +
        geom_line(aes(y = data$prediction, colour = "Vorhersage")) +
        geom_line(aes(y = data$trend, colour = "Typischer Wert")) +
        scale_fill_manual(values = c("MAE" = "blue", "90% Confidence" = "orange"),
                        name = "Schwankungsbereiche") +
        scale_color_manual(values = c("Vorhersage" = "blue", "Typischer Wert" = "red"),
                name = "Vorhersagen") +
        scale_x_date(date_breaks = "1 month", date_labels = "%b") +
        xlab(xlab) +
        ylab(ylab) +
        theme_bw() +
        theme(plot.title = element_text(size = 20, face = "bold"),
            axis.title = element_text(size = 12),
            axis.text.x = element_text(size = 10))

    return(plot)
}

areaDiagram <- function (file, data, lowerLimit, upperLimit, steps, xlab, ylab) {
    plot <- ggplot(data, aes(x = data$date)) +
        ggtitle(getTitle(file)) +
        coord_cartesian(ylim = c(lowerLimit, upperLimit)) +
        scale_y_continuous(breaks = seq(lowerLimit, upperLimit, steps)) +

        geom_area(aes(y = data$lower_bound_confidence_90, fill = "Minimale Erwartung"), alpha = 0.7) +
        geom_area(aes(y = data$upper_bound_confidence_90, fill = "Maximale Erwartung"), alpha = 0.2) +

        geom_line(aes(y = data$trend, colour = "Typischer Wert")) +

        scale_fill_manual(values = c("Minimale Erwartung" = "blue", "Maximale Erwartung" = "orange"),
                        name = "Schwankungsbereiche") +
        scale_color_manual(values = c("Vorhersage" = "blue", "Typischer Wert" = "red"),
                name = "Vorhersagen") +
        scale_x_date(date_breaks = "1 month", date_labels = "%b") +
        xlab(xlab) +
        ylab(ylab) +
        theme_bw() +
        theme(plot.title = element_text(size = 20, face = "bold"),
            axis.title = element_text(size = 12),
            axis.text.x = element_text(size = 10))

    return(plot)
}

