# statistical_computing_ml - Verzeichnisstruktur

## /data
Enthält alle vom DWD bezogenen Daten und Dateien sowie die vom Verarbeitungsprozess generierten Dateien.

**/data/completed**

Enthält aufbereitete historische Daten, gefiltert auf die Zeitspanne die in der Auswertung berücksichtigt werden soll.

**/data/history**

Enthält aufbereitete und gefilterte Daten aus den einzelnen Wetterstationen.

**/data/plots**

Enthält mit R und Python erstellte Grafiken. Zum Beispiel Histogramme über den Wetterverlauf oder Darstellungen der Fehlerverteilung in den neuronalen Netzen.

**/data/source**

Enthält die ursprünglichen Daten Open Data Servers des DWD.

**/data/training**

Enthält die Daten mit denen die neuronalen Netze der Wetterstationen trainiert und validiert werden.

**/data/trend**

Enthält Dateien mit den typischen Tageswerten der Wetterstationen sowie die Prognosen über die einzelnen Wetterfaktoren.

## /scripts
Enthält Python-Skripte zur Datenaufbereitung, zum Training neuronaler Netze und zur Erstellung der Wetterprognosen.

**/scripts/merge.py**

Wird in der Fallstudie unter "Zusammenführen der Daten" beschrieben.

**/scripts/refine.py**

Wird in der Fallstudie unter "Aufbereiten der Daten" beschrieben.

**/scripts/trend.py**

Wird in der Fallstudie unter "Extraktion typischer Daten" beschrieben.

**/scripts/predict_cloudiness.py & /scripts/predict_temperature.py & /scripts/predict_wind.py**

Wird in der Fallstudie unter "Vorhersage neuer Daten" beschrieben.


### /scripts/Wind & Temperature & Cloudiness
Enthält Scripte zur Entwicklung und zum Training neuronaler Netze, die Checkpoints und serialisierten Modelle der trainierten Netze, sowie Reports über die Performance der Netze.
Für die drei Wetterfaktoren liegen jeweils die folgenden Skripte vor. Eventuelle weitere Dateien dienen entweder Entwicklungszwecken oder werden von den folgenden Dateien verwendet.

**/scripts/.../training.py**

Führt das Training eines neuronalen Netzes aus.

**/scripts/.../analyzeErrorDistribution.py**

Statistische Fehleranalyse der neuronalen Netze, um festzustellen ob die Fehlerabweichungen normalverteilt auftreten. Gibt auf Grund der großen Datenmengen keinen Aufschluss über die Normalverteilung.

**/scripts/.../plotErrorDistribution.py**

Erstellt je Wetterstation ein Q-Q-Diagramm über die Werteverteilung der Fehlerabweichungen, zur Interpretation über eine Normalverteilung der Fehler.


## /views
Enthält R-Skripte zur Generierung von Grafiken und Tabellen.

**/views/functions**

Enthält generalisierte Funktionen, die in den anderen R-Skripten häufiger verwendet werden. Zum Beispiel die Generierung einfacher Diagramme oder die Aggregation von DataFrames mit einheitlicher Struktur.

**/views/comparison_plots.R**

Erstellt ein sortiertes Balkendiagramm über den Variabilitätsscore der Wetterstationen.

**/views/comparison_plots.R**

Erstellt eine sortierte Tabelle über den Variabilitätsscore der Wetterstationen.

**/views/forecast.R**

Erstellt für die Wetterstationen eine Wettervorhersage für 2023 über die drei Wetterfaktoren.

**/views/forecast_cloudiness.R**

Erstellt für die Wetterstationen eine Vorhersage über die tagesdurchschnittliche Wolkenbedeckung. Enthält den Mittleren Absoluten Fehler und ein 90 prozentiges Konfidenzintervall als gekennzeichnete Schwankungsbereiche.

**/views/forecast_temperature.R**

Erstellt für die Wetterstationen eine Vorhersage über die tagesdurchschnittliche Temperatur. Enthält den Mittleren Absoluten Fehler und ein 90 prozentiges Konfidenzintervall als gekennzeichnete Schwankungsbereiche.

**/views/forecast_wind.R**

Erstellt für die Wetterstationen eine Vorhersage über die tagesdurchschnittliche Windgeschwindigkeit. Enthält den Mittleren Absoluten Fehler und ein 90 prozentiges Konfidenzintervall als gekennzeichnete Schwankungsbereiche.

**/views/historical.R**

Erstellt für die Wetterfaktoren vergleichende Histogramme zwischen den Wetterstationen über die letzten 3 Jahre.
Erstellt jeweils ein Diagramm mit geglätteten Plots für alle Wetterstationen sowie eine Grafik mit ungeglättetem Verlauf über einzelne Stationen.
