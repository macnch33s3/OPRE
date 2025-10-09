# Created on Tue May 28 10:03:53 2024
# katrin.huegel

from ortools.linear_solver import pywraplp
import pandas as pd

def main():
    # Create Model
    solver_name='SCIP'
    solver = pywraplp.Solver.CreateSolver(solver_name)
    solver.EnableOutput()

    # Datei mit Parametern öffnen
    xlsx = pd.ExcelFile("./LB1_LP_SAMPLE/UMP12_PARAMS.xlsx")

    # Nachfrage aus Excel einlesen
    d_df = xlsx.parse(sheet_name="Nachfrage")
    d_data = d_df.iloc[:,1]
    d = d_data.values.tolist()
    anz_K = len(d)

    f_df = xlsx.parse(sheet_name="Produktionskapazität")
    f_data = f_df.iloc[:,1]
    f = f_data.values.tolist()
    anz_P = len(f)

    # Transportkosten aus Excel einlesen
    c_df= xlsx.parse(sheet_name='Transportkosten') # Daten aus dem Sheet ziehen, das benötigten Infos enthält
    col_K = list(range(1, anz_K+1)) # Spalten, in denen die Kunden-Info steht
    c_data = c_df.iloc[:,col_K]  # Spalten für Kunden (ohne Spalte Standortbezeichnung)
    c = c_data.values.tolist()  

    I = list(range(anz_P))  # Index Produktionsstandorte

    J = list(range(anz_K))  # Index für Kunden

    # Define upper bound Entscheidungsvariablen-Wert (optional, Wertebereich reduzieren)
    X_ub = sum(d)

    #define Entscheidungsvariable
    X = {}
    for i in I:
        for j in J:
            X[(i,j)] = solver.IntVar(0,X_ub, 'task_i%ij%i'%(i,j))  # lB=0 ist schon definiert
            
    # NB1: Nachfrage erfüllen
    for j in J:
        solver.Add(sum(X[(i,j)] for i in I)>= d[j])

    #NB2: Kapazität einhalten
    for i in I:
        solver.Add(sum(X[(i,j)] for j in J)<=f[i])
        
    # Zielfunktion
    solver.Minimize(sum(X[(i,j)] * c[i][j] for i in I for j in J))

    # solve the model
    status = solver.Solve()

    if status ==pywraplp.Solver.OPTIMAL:
        print("Lösung:")
        print("Objective Value:", solver.Objective().Value())
        for i in I:
            for j in J:
                print("X_{}_{} = {}". format(i, j, X[(i,j)].solution_value()))
    else:
        print("the Problem does not have an optimal solution")

if __name__ == "__main__":
    main()
