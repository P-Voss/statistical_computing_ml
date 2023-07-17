
source("views/functions/completePlot.R")

# Maße und Auflösung per Experimentieren finden
savePlot <- function (plot, filepath) {
    png(filepath, res = 150, height = 860, width = 1900)
    print(plot)
    dev.off()
}

plot <- generatePlot("Arkona")
print(plot)
# savePlot(plot, "data/plots/forecasts/complete_saved_Arkona.png")

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

