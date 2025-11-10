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