# Fallstudie Kombinatorische Optimierung
Dieses Verzeichnis ist Ihr Arbeitsverzeichnis für die Fallstudie. Hier entwickeln Sie den Code für Ihre gewählte Problemstellung.

Zusätzlich finden Sie in den Unterverzeichnissen die Informationen und Testinstanzen zu den verschiedenen Projektideen im Lernblock Kombinatorische Optimierung. 

**Tipps:** 
- Wenn Sie diese Datei in VSCode lesen und sie hässlich aussieht, liegt das vermutlich daran, dass Sie sie als Textdatei anzeigen lassen. Drücken Sie dann Crtl+Shift+V, um in die Visualisierungs-View zu wechseln.
- Um den Sourcecode hinter einer Funktion im Jupyter Notebook anzuzeigen, drücken Sie Sie in VSCode einfach die Ctrl-Taste und clicken Sie mit dem Mousepointer auf den Funktionsnamen. Danach kehren Sie mit Alt+'<-' (Rückwärtspfeil-Taste) wieder zum zuletzt angezeigten Fenster (d.h. dieses Jupyter Notebook) zurück.


## Themenübersicht
Nachfolgend werden die einzelnen Projektideen vorgestellt. Zu jeder Projektidee finden Sie in diesem Verzeichnis ein Unterverzeichnis mit 
- **Probleminstanzen**: Dies sind die zu lösenden Problemstellungen, beschrieben in menschenlesbarer Form als Textdatei.
- **Data-Import-Skript**:  Dieses Python Skript enthält eine Reader-Funktion zum Einlesen der Probleminstanzen für das jeweilige Problem.  
- **Jupyter Notebook**: Dieses Jupyter Notebook enthält Erklärungen zur Problemstellung und zur Anwendung der Reader-Funktion zum Einlesen von Probleminstanzen. 

Ob Sie für Ihre Entwicklungen ein eigenes Jupyter Notebook entwickeln oder lieber ein standalone Python-Skript schreiben, ist Ihre Wahl. Beide Vorgehensweisen haben ihre Vor-/Nachteile.


### Subset-Sum-Problem
_Unterverzeichnis: "./subset_sum_problem"_

Ein Rucksack mit einem bestimmten Volumen soll möglichst effizient gepackt werden:
Aus Objekten mit unterschiedlichem Volumen soll eine Teilmenge so ausgewählt werden, dass das Volumen
unter Berücksichtigung der Volumenbeschränkung möglichst maximal ausgeschöpft wird.

### 1D-Bin-Packing-Problem (bin_packing_1d)
_Unterverzeichnis: "./bin_packing_1d"_

Pakete mit variabler Höhe und konstanter Grundfläche müssen in unbeschränkt zur Verfügung stehende Versandkartons von fixer Höhe verpakt werden, wobei die Anzahl benötigter Kartons minimiert werden soll.

### 2D-Bin-Packing-Problem (bin_packing_2d)
_Unterverzeichnis: "./bin_packing_2d"_

Eine bestimmte Anzahl rechteckiger Schachteln mit unterschiedlichen Dimensionen (x,y) sollen möglichst effizient in unbeschränkt zur Verfügung stehende rechteckige Versandkartons mit ebenfalls vorgegebenen Dimensionen gepackt werden. Möglichst wenige Versandkartons sollen gebraucht werden.

### Facility Location Problem
_Unterverzeichnis: "./facility_location_problem"_

Aus unterschiedlichen möglichen Standorten von Feuerwehrdepots sollen jene ausgewählt werden, dass jede Wohnung von mindestens einem Depot innerhalb einer kritischen Distanz erreichbar ist. Die Auswahl soll so getroffen werden, dass die Kosten für eröffnete Feuerwehrdepots minimal sind.

### Traveling Salesman Problem  (bin_packing_1d)
_Unterverzeichnis: "./facility_location_problem"_

Der Ablauf der Bohrungen von elektronischen Leiterplatten soll optimiert werden, so dass der Bohrkopf eine möglichst geringe Distanz zurücklegen muss. 

### Parallel Machine Scheduling Problem
Eine bekannte Liste von Aufträgen mit gegebener Dauer soll auf eine ebenfalls bekannte Anzahl identischer Maschinen aufgeteilt werden, so dass die Gesamtproduktionszeit minimal wird.

