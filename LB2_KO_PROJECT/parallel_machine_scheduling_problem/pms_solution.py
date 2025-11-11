import numpy as np
from ppl_reader import read_ppl_file    # vorhergeschriebenes modul importieren
from typing import List, Tuple, Dict    # Type hints
import copy                             # library die deepcopy und shallowcopy beeinhalted

# ============================================================================
# HILFSFUNKTIONEN
# ============================================================================

def calculate_makespan(assignment: List[List[int]], job_durations: List[int]) -> int:   # Definition für die Berechnung der maximalen Maschinenlast für gegebene Zuweisung
                                                                                        # returns makespan (maximale Gesamtdauer über alle Maschinen) 
    machine_loads = [] # kreiere eine leere Liste um die machine_loads hineinzuspeichern 
    for machine_jobs in assignment:
        load = 0
        for job in machine_jobs:
            load += job_durations[job]
        machine_loads.append(load) # neuer load in liste machine_loads am Ende hinzufügen 

    if machine_loads:
        return max(machine_loads)
    else:
        return 0

    # machine_loads = [sum(job_durations[job] for job in machine_jobs) 
                    #  for machine_jobs in assignment]
    # return max(machine_loads) if machine_loads else 0


def get_machine_loads(assignment: List[List[int]], job_durations: List[int]) -> List[int]: # Last für jede Maschine berechnen
                                                                                            # returns list: last für jede Maschine
    machine_loads = []

    for machine_jobs in assignment:
        load = 0
        for job in machine_jobs:
            load += job_durations[job]
        machine_loads.append(load)

    return machine_loads

# Ausführlichere Variante von:
    # return [sum(job_durations[job] for job in machine_jobs) 
    #         for machine_jobs in assignment]


def print_solution(assignment: List[List[int]], job_durations: List[int], # Lösung formatiert ausgeben
                   method_name: str = "") -> None:

    makespan = calculate_makespan(assignment, job_durations)
    loads = get_machine_loads(assignment, job_durations)
    
    print(f"\n{'='*70}")
    if method_name:
        print(f"Methode: {method_name}")
    print(f"{'='*70}")
    print(f"Makespan: {makespan}")
    print(f"\nMaschinen-Lasten: {loads}")
    print(f"\nZuweisung:")

    i = 0
    for machine_jobs in assignment:
        job_info = ""

        for j in machine_jobs:
            job_info += f"J{j}({job_durations[j]}), "
        # das letzte Komma und Leerzeichen entfernen
        job_info = job_info[:-2] if job_info else ""
        print(f"  Maschine {i + 1}: {job_info} -> Last: {loads[i]}")
        i += 1

    # for i, machine_jobs in enumerate(assignment):
        # job_info = [f"J{j}({job_durations[j]})" for j in machine_jobs]
        # print(f"  Maschine {i+1}: {', '.join(job_info)} -> Last: {loads[i]}")

    print(f"{'='*70}\n")


# ============================================================================
# KONSTRUKTIONSHEURISTIKEN
# ============================================================================

def greedy_lpt(num_machines: int, job_durations: List[int]) -> List[List[int]]: # greedy longest processing time
                                                                                # Sortiert Jobs absteigend nach Dauer und weist jeden Job der am wenigsten belasteten Maschine zu.
                                                                                # returns job-zuweisung als list[list[int]]

    # Jobs nach Dauer sortieren (absteigend)
    jobs_sorted = sorted(range(len(job_durations)), 
                        key=lambda j: job_durations[j], reverse=True)
    
    # Initialisierung
    assignment = [[] for _ in range(num_machines)]
    machine_loads = [0] * num_machines
    
    # Jobs zuweisen
    for job in jobs_sorted:
        min_machine = min(range(num_machines), key=lambda m: machine_loads[m])
        assignment[min_machine].append(job)
        machine_loads[min_machine] += job_durations[job]
    
    return assignment


def greedy_spt(num_machines: int, job_durations: List[int]) -> List[List[int]]: # greedy shortest processing time / gleich wie greedy_lpt nur ohne reverse
                                                                                # Sortiert Jobs aufsteigend nach Dauer.
                                                                                # returns job-zuweisung als list[list[int]]

    # Jobs nach Dauer sortieren (aufsteigend) / gleich wei bei greedy_lpt
    jobs_sorted = sorted(range(len(job_durations)), 
                        key=lambda j: job_durations[j]) # hier ohne reverse
    
    # Initialisierung
    assignment = [[] for _ in range(num_machines)]
    machine_loads = [0] * num_machines
    
    # Jobs zuweisen
    for job in jobs_sorted:
        min_machine = min(range(num_machines), key=lambda m: machine_loads[m])
        assignment[min_machine].append(job)
        machine_loads[min_machine] += job_durations[job]
    
    return assignment


def balanced_greedy(num_machines: int, job_durations: List[int]) -> List[List[int]]:    # Balanziert greedy-heuristiken
                                                                                        # weist jobs sequentiell der am wenigsten belasteten Maschine zu (ohne Sortierung)
                                                                                        # returns job-zuweisung als list[list[int]]
    # Initialisierung
    assignment = [[] for _ in range(num_machines)]
    machine_loads = [0] * num_machines
    
    # Jobs in ursprünglicher Reihenfolge zuweisen
    for job in range(len(job_durations)): # jobs werden hier nicht sortiert, es wird nur durch die range iiteriert
        min_machine = min(range(num_machines), key=lambda m: machine_loads[m])
        assignment[min_machine].append(job)
        machine_loads[min_machine] += job_durations[job]
    
    return assignment


# ============================================================================
# VERBESSERUNGSHEURISTIKEN
# ============================================================================

def local_search_swap(assignment: List[List[int]], job_durations: List[int],    # Local-Search durch Swap
                      max_iterations: int = 1000) -> List[List[int]]:           # returns Verbesserte job-zuweisung als List[list[int]]
    """
    Lokale Suche mit Swap-Nachbarschaft.
    Tauscht Jobs zwischen zwei Maschinen, wenn dies den Makespan verbessert.
    
    Args:
        assignment: Initiale Job-Zuweisung
        job_durations: Liste der Job-Dauern
        max_iterations: Maximale Anzahl Iterationen
    
    Returns:
        Verbesserte Job-Zuweisung
    """
    current_assignment = copy.deepcopy(assignment) # deepcopy erstellt vollständige Kopie, mit allen verschachtelten Elementen
    current_makespan = calculate_makespan(current_assignment, job_durations)
    improved = True
    iterations = 0
    
    while improved and iterations < max_iterations: 
        improved = False
        iterations += 1
        
        # Probiere alle Maschinenpaare
        for m1 in range(len(current_assignment)):
            for m2 in range(m1 + 1, len(current_assignment)):
                # Probiere alle Job-Paare zwischen m1 und m2
                for i, job1 in enumerate(current_assignment[m1]):
                    for j, job2 in enumerate(current_assignment[m2]):
                        # Erstelle Nachbar durch swap
                        neighbor = copy.deepcopy(current_assignment)
                        neighbor[m1][i], neighbor[m2][j] = neighbor[m2][j], neighbor[m1][i]
                        
                        neighbor_makespan = calculate_makespan(neighbor, job_durations)
                        
                        if neighbor_makespan < current_makespan:
                            current_assignment = neighbor
                            current_makespan = neighbor_makespan
                            improved = True
                            break
                    if improved:
                        break
                if improved:
                    break
            if improved:
                break
    
    return current_assignment


def local_search_move(assignment: List[List[int]], job_durations: List[int],    # Local-Search durch Move
                      max_iterations: int = 1000) -> List[List[int]]:           # returns Verbesserte Job-Zuweisung als List[list[int]]
    """
    Lokale Suche mit Move-Nachbarschaft.
    Verschiebt einzelne Jobs zu einer anderen Maschine, wenn dies den Makespan verbessert.
    
    Args:
        assignment: Initiale Job-Zuweisung
        job_durations: Liste der Job-Dauern
        max_iterations: Maximale Anzahl Iterationen
    
    Returns:
        Verbesserte Job-Zuweisung
    """
    current_assignment = copy.deepcopy(assignment)
    current_makespan = calculate_makespan(current_assignment, job_durations)
    improved = True
    iterations = 0
    
    while improved and iterations < max_iterations:
        improved = False
        iterations += 1
        
        # Probiere alle Jobs zu verschieben
        for m_from in range(len(current_assignment)):
            for job_idx, job in enumerate(current_assignment[m_from]):
                # Probiere alle anderen Maschinen
                for m_to in range(len(current_assignment)):
                    if m_from == m_to:
                        continue
                    
                    # Erstelle Nachbar durch Verschieben
                    neighbor = copy.deepcopy(current_assignment)
                    neighbor[m_from].pop(job_idx)
                    neighbor[m_to].append(job)
                    
                    neighbor_makespan = calculate_makespan(neighbor, job_durations)
                    
                    if neighbor_makespan < current_makespan:
                        current_assignment = neighbor
                        current_makespan = neighbor_makespan
                        improved = True
                        break
                if improved:
                    break
            if improved:
                break
    
    return current_assignment


def simulated_annealing(assignment: List[List[int]], job_durations: List[int],  # simulated annealing - mit einer
                       initial_temp: float = 100.0, cooling_rate: float = 0.95, # abnehmender Wahrscheinlichkeit werden in der LS auch schlechtere Lösungen akzeptiert.
                       max_iterations: int = 1000) -> List[List[int]]:          # returns beste gefunden job-zuweisung als List[list[inst]]
    
    """
    Simulated Annealing Metaheuristik.
    Akzeptiert auch schlechtere Lösungen mit einer temperaturabhängigen Wahrscheinlichkeit.
    
    Args:
        assignment: Initiale Job-Zuweisung
        job_durations: Liste der Job-Dauern
        initial_temp: Starttemperatur
        cooling_rate: Abkühlungsrate (0 < cooling_rate < 1)
        max_iterations: Maximale Anzahl Iterationen
    
    Returns:
        Beste gefundene Job-Zuweisung
    """
    current = copy.deepcopy(assignment)
    current_makespan = calculate_makespan(current, job_durations)
    best = copy.deepcopy(current)
    best_makespan = current_makespan
    
    temp = initial_temp
    
    for iteration in range(max_iterations):
        # Erzeuge Nachbar (zufällig: Move oder Swap)
        neighbor = copy.deepcopy(current)
        
        if np.random.random() < 0.5 and len([j for m in neighbor for j in m]) > 1:
            # Move: Verschiebe zufälligen Job
            m_from = np.random.randint(len(neighbor))
            while len(neighbor[m_from]) == 0:
                m_from = np.random.randint(len(neighbor))
            
            job_idx = np.random.randint(len(neighbor[m_from]))
            job = neighbor[m_from].pop(job_idx)
            m_to = np.random.randint(len(neighbor))
            neighbor[m_to].append(job)
        else:
            # Swap: Tausche zwei Jobs zwischen Maschinen
            machines_with_jobs = [i for i, m in enumerate(neighbor) if len(m) > 0]
            if len(machines_with_jobs) >= 2:
                m1, m2 = np.random.choice(machines_with_jobs, 2, replace=False)
                if len(neighbor[m1]) > 0 and len(neighbor[m2]) > 0:
                    i1 = np.random.randint(len(neighbor[m1]))
                    i2 = np.random.randint(len(neighbor[m2]))
                    neighbor[m1][i1], neighbor[m2][i2] = neighbor[m2][i2], neighbor[m1][i1]
        
        neighbor_makespan = calculate_makespan(neighbor, job_durations)
        delta = neighbor_makespan - current_makespan    # misst wieviel schlechter oder besser die neue Lösung (neighbour)
                                                        # im Vergleich zur aktuellen Lösung (current) ist
        
        # Akzeptanzkriterium
        if delta < 0 or np.random.random() < np.exp(-delta / temp): # delta < 0, dann ist neue Lösung besser -> wird akzeptiert
            current = neighbor                                      # delta > 0, dann ist neue Lösung schlechter -> kann akzeptiert werden
            current_makespan = neighbor_makespan                    # mit einer Wahrscheinlichkeit
            
            if current_makespan < best_makespan:
                best = copy.deepcopy(current)
                best_makespan = current_makespan
        
        # Abkühlung
        temp *= cooling_rate
    
    return best


# ============================================================================
# HAUPTPROGRAMM
# ============================================================================

def solve_instance(filename: str, use_all_methods: bool = True) -> Dict[str, int]:  # Löst eine Problem-Instanz mit verschiedenen Methoden
                                                                                    # returns Dictonary mit Ergebnissen aller Methoden

    print(f"\n{'#'*70}")
    print(f"# Problem-Instanz: {filename}")
    print(f"{'#'*70}\n")
    
    # Daten einlesen
    num_machines, job_durations = read_ppl_file(filename)
    num_jobs = len(job_durations)
    total_duration = sum(job_durations)
    lower_bound = int(np.ceil(total_duration / num_machines))
    
    # Parameter in Console printen
    print(f"Anzahl Maschinen: {num_machines}")
    print(f"Anzahl Jobs: {num_jobs}")
    print(f"Job-Dauern: {job_durations}")
    print(f"Gesamt-Dauer: {total_duration}")
    print(f"Theoretische Untergrenze (Makespan): {lower_bound}")
    
    results = {}
    
    # LPT Heuristik
    print("\n" + "="*70)
    print("1. LPT (Longest Processing Time) Heuristik")
    print("="*70)
    lpt_solution = greedy_lpt(num_machines, job_durations)
    lpt_makespan = calculate_makespan(lpt_solution, job_durations)
    print_solution(lpt_solution, job_durations, "LPT")
    results['LPT'] = lpt_makespan
    
    if use_all_methods:
        # SPT Heuristik
        spt_solution = greedy_spt(num_machines, job_durations)
        spt_makespan = calculate_makespan(spt_solution, job_durations)
        print_solution(spt_solution, job_durations, "SPT (Shortest Processing Time)")
        results['SPT'] = spt_makespan
        
        # Balancierte Greedy
        balanced_solution = balanced_greedy(num_machines, job_durations)
        balanced_makespan = calculate_makespan(balanced_solution, job_durations)
        print_solution(balanced_solution, job_durations, "Balanced Greedy")
        results['Balanced'] = balanced_makespan
    
    # Lokale Suche (Move) auf bester Ausgangslösung
    print("\n" + "="*70)
    print("2. Lokale Suche mit Move-Nachbarschaft")
    print("="*70)
    ls_move_solution = local_search_move(lpt_solution, job_durations)
    ls_move_makespan = calculate_makespan(ls_move_solution, job_durations)
    print_solution(ls_move_solution, job_durations, "LPT + Local Search (Move)")
    results['LPT + LS Move'] = ls_move_makespan
    
    # Lokale Suche (Swap)
    print("\n" + "="*70)
    print("3. Lokale Suche mit Swap-Nachbarschaft")
    print("="*70)
    ls_swap_solution = local_search_swap(lpt_solution, job_durations)
    ls_swap_makespan = calculate_makespan(ls_swap_solution, job_durations)
    print_solution(ls_swap_solution, job_durations, "LPT + Local Search (Swap)")
    results['LPT + LS Swap'] = ls_swap_makespan
    
    # Simulated Annealing
    print("\n" + "="*70)
    print("4. Simulated Annealing")
    print("="*70)
    sa_solution = simulated_annealing(lpt_solution, job_durations, 
                                     initial_temp=100, cooling_rate=0.95, 
                                     max_iterations=2000)
    sa_makespan = calculate_makespan(sa_solution, job_durations)
    print_solution(sa_solution, job_durations, "Simulated Annealing")
    results['Simulated Annealing'] = sa_makespan
    
    # Zusammenfassung
    print("\n" + "#"*70)
    print("# ZUSAMMENFASSUNG")
    print("#"*70)
    print(f"\nTheoretische Untergrenze: {lower_bound}")
    print("\nErgebnisse aller Methoden:")
    for method, makespan in sorted(results.items(), key=lambda x: x[1]):
        gap = ((makespan - lower_bound) / lower_bound * 100) if lower_bound > 0 else 0
        print(f"  {method:25s}: {makespan:.5f}  (Gap: {gap:5.1f}%)")
        # method:25s ->  string mit fester Breite 25
        # makespan:.5f -> Float mit fester Breite 5 Nachkommastellen
        # gap:5.1f ->    Float mit Nachkommastelle (Gesamtbreite 5, Nachkomastelle 1, f besagt float)
    
    best_method = min(results.items(), key=lambda x: x[1])
    print(f"\nBeste Methode: {best_method[0]} mit Makespan {best_method[1]}")
    
    return results

# ============================================================================
# BEISPIELAUFRUF
# ============================================================================

if __name__ == "__main__":
    # Einzelne Instanz lösen
    solve_instance("data/PRODPLAN_M2_J5.ppl")
    
    # Mehrere Instanzen lösen
    # instances = [
    #    "data/PRODPLAN_M2_J5.ppl",
    #    "data/PRODPLAN_M2_J8.ppl",
    #     "data/PRODPLAN_M2_J21.ppl",
    #     "data/PRODPLAN_M4_J32.ppl",
    #     "data/PRODPLAN_M2_J4_test.ppl",
    #     "data/PRODPLAN_M2_J4_test2.ppl"
    #]
    #
    #for instance in instances:
    #    try:
    #        solve_instance(instance, use_all_methods=True)
    #    except Exception as e:
    #        print(f"Fehler bei {instance}: {e}")