from ortools.linear_solver import pywraplp

def main():
     # UMP16: Zuordnungsproblem Aufgaben / Arbeiter
     # Create the model.
     solver_name = 'SCIP'  # alternatively: 'GUROBI_MIP'
     solver = pywraplp.Solver.CreateSolver(solver_name)
     solver.EnableOutput()
     
     # define parameters
     c = [[200, 180, 170, 140, 160],  # costs if employee i performs task j
           [210, 190, 140, 160, 150],
           [190, 120, 150, 180, 210],
           [160, 170, 210, 140, 120],
           [130, 140, 120, 140, 150]]
     
     # determine index sets
     I = list(range(len(c)))  # all employees
     J = list(range(len(c[0])))  # all tasks
     
     # declare decision variables
     X = {}
     for i in I:
          for j in J:
               X[(i, j)] = solver.BoolVar('task_i%ij%i' % (i, j))
     
     # constraint 1: Every employee must solve exactly one task
     for i in I:
          solver.Add(sum(X[(i, j)] for j in J) == 1)
     
     # constraint 2: Every task must be performed exactly once
     for j in J:
          solver.Add(sum(X[(i, j)] for i in I) == 1)
     
     # objective function
     solver.Minimize(sum(X[(i, j)] * c[i][j] for i in I for j in J))
     
     # solve the model
     status = solver.Solve()
     
     if status == pywraplp.Solver.OPTIMAL:
          print("Solution:")
          print("Objective value =", solver.Objective().Value())
          for i in I:
               for j in J:
                    print(f"X_{i}_{j} = {int(X[(i, j)].solution_value())}")
     else:
          print("The problem does not have an optimal solution.")


if __name__ == "__main__":
    main()
