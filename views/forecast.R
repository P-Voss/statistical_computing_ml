
source("views/functions/completePlot.R")

# Maße und Auflösung per Experimentieren finden
savePlot <- function (plot, name) {
    filepath <- paste0("data/plots/forecasts/complete_", name, ".png")
    png(filepath, res = 200, height = 600, width = 900)
    print(plot)
    dev.off()
}

plot <- generatePlot("Arkona")
print(plot)

plot <- generatePlot("Boltenhagen")
print(plot)

plot <- generatePlot("Cuxhaven")
print(plot)

plot <- generatePlot("Emden")
print(plot)

plot <- generatePlot("Fehmarn")
print(plot)

plot <- generatePlot("Hattstedt")
print(plot)

plot <- generatePlot("Hohwacht")
print(plot)

plot <- generatePlot("Karlshagen")
print(plot)

plot <- generatePlot("Konstanz")
print(plot)

plot <- generatePlot("Ueckermuende")
print(plot)

