import numpy as np
from ppl_reader import read_ppl_file  # Funktion für Import der Daten
from typing import List, Tuple, Dict
import copy

# Import der Daten
num_machines, job_durations = read_ppl_file("data/PRODPLAN_M2_J8.ppl")

print("Anzahl Maschinen:", num_machines)
print("Dauer der Jobs:", job_durations)


assignment = [
    [0, 3],      # Maschine 0 bearbeitet Jobs 0 und 3
    [1, 2, 4]    # Maschine 1 bearbeitet Jobs 1, 2 und 4
]

#------------------------------------------------------

# Hilfsfunktionen initialisieren
# Produktionsdauer
def calculate_makespan(assignment: List[List[int]], job_durations: List[int]): # Gibt aus: int

    machine_loads = []
    for machine_jobs in assignment:
        total = 0
        for job in machine_jobs:
            total += job_durations[job]
        machine_loads.append(total)

    return max(machine_loads) if machine_loads else 0

# Maschinenauslaustung
def get_machine_loads(assignment: List[List[int]], job_durations: List[int]): # Gibt aus: List[int]
    return [sum(job_durations[job] for job in machine_jobs) 
            for machine_jobs in assignment]

# Lösung ausgeben
def print_solution(assignment: List[List[int]], job_durations: List[int], 
                   method_name: str = ""):
    
    makespan = calculate_makespan(assignment, job_durations)
    loads = get_machine_loads(assignment, job_durations)
    
    if method_name:
        print(f"Methode: {method_name}")

    print(f"Makespan: {makespan}")
    print(f"\nMaschinen-Lasten: {loads}")
    print(f"\nZuweisung:")
    for i, machine_jobs in enumerate(assignment):
        job_info = [f"J{j}({job_durations[j]})" for j in machine_jobs]
        print(f"  Maschine {i+1}: {', '.join(job_info)} → Last: {loads[i]}")

#------------------------------------------------------

# Konstruktionsheuristiken

def greedy_lpt(job_durations, num_machines): # lpt = longest processing time
    # Sort jobs in descending order based on duration
    sorted_jobs = sorted(job_durations.items(), key=lambda x: x[1], reverse=True)

    # Initialize machine loads and assignment
    machine_loads = [0] * num_machines
    assignment = {m + 1: [] for m in range(num_machines)}

    # Assign each job to the least loaded machine
    for job_id, duration in sorted_jobs:
        min_machine = machine_loads.index(min(machine_loads))
        assignment[min_machine + 1].append(job_id)
        machine_loads[min_machine] += duration

    return assignment, machine_loads

def greedy_spt(job_durations, num_machines):
                   # Sort jobs in ascending order based on duration
    sorted_jobs = sorted(job_durations.items(), key=lambda x: x[1]) # Die selbe KH wie greedy_lpt einfach nicht reversed

    # Initialize machine loads and assignment
    machine_loads = [0] * num_machines
    assignment = {m + 1: [] for m in range(num_machines)}

    # Assign each job to the least loaded machine
    for job_id, duration in sorted_jobs:
        min_machine = machine_loads.index(min(machine_loads))
        assignment[min_machine + 1].append(job_id)
        machine_loads[min_machine] += duration

    return assignment, get_machine_loads

def balanced_greedy(job_durations, num_machines):
    # Initialize machine loads and assignment
    machine_loads = [0] * num_machines
    assignment = {m + 1: [] for m in range(num_machines)}

    # Sequentially assign each job to the least loaded machine
    for job_id, duration in job_durations.items():
        min_machine = machine_loads.index(min(machine_loads))
        assignment[min_machine + 1].append(job_id)
        machine_loads[min_machine] += duration

    return assignment, get_machine_loads

#------------------------------------------------------

# LS - Verbesserungsheuristiken
def local_search_swap(assignment, job_durations, # Lokale Suche mit Swap-Nachbarschaft
                      max_iterations = 1000):

    current_assignment = copy.deepcopy(assignment)
    current_makespan = calculate_makespan(current_assignment, job_durations)
    improved = True
    iterations = 0
    
    while improved and iterations < max_iterations:
        improved = False
        iterations += 1
        
        # Probiere alle Paare von Maschinen
        for m1 in range(len(current_assignment)):
            for m2 in range(m1 + 1, len(current_assignment)):
                # Probiere alle Job-Paare zwischen m1 und m2
                for i, job1 in enumerate(current_assignment[m1]):
                    for j, job2 in enumerate(current_assignment[m2]):
                        # Erstelle Nachbar durch Tausch
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

def local_search_move(assignment, job_durations,  # Local Search mit Move-Nachbarschaft
                      max_iterations = 1000):
    
    current_assignment = copy.deepcopy(assignment) # deepcopy erstellt eine vollständige und unabhängige Kopie von einem Objekt (und deren verschachtelten Objekten) in assignments.
    current_makespan = calculate_makespan(current_assignment, job_durations)
    improved = True
    iterations = 0
    
    while improved and iterations < max_iterations:
        improved = False
        iterations += 1 # iterations hoch zählen
        
        # Probiere alle Jobs zu verschieben
        for m_from in range(len(current_assignment)):
            for job_idx, job in enumerate(current_assignment[m_from]):
                # Probiere alle anderen Maschinen
                for m_to in range(len(current_assignment)):
                    if m_from == m_to:
                        continue
                    
                    # Erstelle Nachbar durch Move
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

def simulated_annealing(assignment, job_durations, # Simmulated Annealing Heuristik - Akzeptiert auch schlechtere Lösungen
                       initial_temp: 100.0, cooling_rate: 0.95, max_iterations: 1000):
    
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
        delta = neighbor_makespan - current_makespan
        
        # Akzeptanzkriterium
        if delta < 0 or np.random.random() < np.exp(-delta / temp):
            current = neighbor
            current_makespan = neighbor_makespan
            
            if current_makespan < best_makespan:
                best = copy.deepcopy(current)
                best_makespan = current_makespan
        
        # Abkühlung
        temp *= cooling_rate
    
    return best

#------------------------------------------------------

# Hauptprogramm
def solve_instance(filename: str, use_all_methods: bool = True):

    print(f"\n{'#'*70}")
    print(f"# Problem-Instanz: {filename}")
    print(f"{'#'*70}\n")
    
    # Daten einlesen
    num_machines, job_durations = read_ppl_file(filename)
    num_jobs = len(job_durations)
    total_duration = sum(job_durations)
    lower_bound = int(np.ceil(total_duration / num_machines))
    
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
        print(f"  {method:25s}: {makespan:6d}  (Gap: {gap:5.1f}%)")
    
    best_method = min(results.items(), key=lambda x: x[1])
    print(f"\nBeste Methode: {best_method[0]} mit Makespan {best_method[1]}")
    
    return results

if __name__ == "__main__":
    # Beispiel: Löse eine oder mehrere Instanzen
    
    # Einzelne Instanz lösen
    solve_instance("data/PRODPLAN_M2_J5.ppl")
    
    # Mehrere Instanzen lösen (auskommentiert)
    # instances = [
    #     "data/PRODPLAN_M2_J5.ppl",
    #     "data/PRODPLAN_M2_J8.ppl",
    #     "data/PRODPLAN_M2_J21.ppl",
    #     "data/PRODPLAN_M4_J32.ppl",
    #     "data/PRODPLAN_M2_J4_test.ppl",
    #     "data/PRODPLAN_M2_J4_test2.ppl"
    # ]
    # 
    # for instance in instances:
    #     try:
    #         solve_instance(instance, use_all_methods=True)
    #     except Exception as e:
    #         print(f"Fehler bei {instance}: {e}")