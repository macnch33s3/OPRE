# Operations Research Skripte
Dieses Projekt stellt Python-Skripte und Jupyter Notebooks bereit, welche Sie z.T. für die verschiedenen Lernblöcke der Vorlesung, den Übungen und der Fallstudie verwenden können. 

**Hinweis:** Wenn Sie diese Datei in VSCode lesen und sie hässlich aussieht, liegt das vermutlich daran, dass Sie sie als Textdatei anzeigen lassen. Drücken Sie dann Crtl+Shift+V, um in die Visualisierungs-View zu wechseln.

Das Projekt beinhaltet Unterverzeichnisse für alle Lernblöcke:

- **LB1_LP_SAMPLE:** Hier finden Sie Skripte und Jupyter Notebooks für die Übungen des ersten Lernblocks zur Linearen Programmierung.

- **LB2_KO_PROJECT:** Hier finden Sie Skripte und Jupyter Notebooks für die Unterstützung in der Fallstudie zur Kombinatorischen Optimierung sowie alle Beispielskripte und Heuristiken im Zusammenhang mit dem Knapsack-Problem.

- **LB3_GT_SAMPLE:** Hier finden Sie Skripte und Jupyter Notebooks für die Übungen des dritten Lernblocks zur Graphentheorie.
-----------------------------------------------------------------------------------------------------------------------------
# Fallstudie - Parallel Machine Scheduling Problem

**Voraussetzungen**
-----
- Git installiert
- Python (empfohlen: 3.13.1)

**Repo klonen**
-----
1. Repository klonen:
```bash
git clone https://github.com/macnch33s3/OPRE.git
```
2. In das Projektverzeichnis wechseln:
```bash
cd OPRE
```
3. In ../OPRE-main/LB2_KO_PROJECT/parallel_machine_scheduling_problem/pms_solution.py finden:
```bash
cd ../OPRE-main/LB2_KO_PROJECT/parallel_machine_scheduling_problem/
```
4. Falls nötig numpy und copy modul installieren mit pip oder uv
```bash
pip install numpy
```
```bash
uv init
uv add numpy
uv add copy
uv sync
```

**Daten**
-----
- Falls Daten benötigt werden (CSV, Modelle o.ä.), beschreibe:
  - wo die Daten heruntergeladen werden können (Links),
  - in welchem Verzeichnis sie abgelegt werden müssen, z. B. `data/` (gitignore prüfen),
  - Beispiel: Lege `data/input.csv` in `data/` ab.

Projektstruktur (Beispiel)
--------------------------
Passe diesen Abschnitt an die tatsächliche Struktur an:
```
pms_solution/         — Paket / Quellcode
  ├─ __init__.py
  ├─ main.py           — Einstiegspunkt
  ├─ config.py         — Konfiguration
  └─ utils/            — Hilfsfunktionen
notebooks/            — Jupyter‑Notebooks (falls vorhanden)
data/                 — (nicht versionierte) Eingabedaten
requirements.txt
README.md
```
