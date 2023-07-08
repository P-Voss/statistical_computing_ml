
transformToMaxValues <- function(data) {
    max_values <- data %>%
      group_by(date) %>%
      summarise_all(max, na.rm = TRUE)
    max_values$date <- as.Date(max_values$date)
    return(max_values)
}


transformToMinValues <- function(data) {
    min_values <- data %>%
      group_by(date) %>%
      summarise_all(min, na.rm = TRUE)
    min_values$date <- as.Date(min_values$date)
    return(min_values)
}


transformToAvgValues <- function(data) {
    avg_values <- data %>%
        group_by(date) %>%
        summarise_all(mean, na.rm = TRUE)
    avg_values$date <- as.Date(avg_values$date)
    return(avg_values)
}
