from ortools.linear_solver import pywraplp

def main():
    # Create the model.
    solver_name = 'SCIP' # alternatively: 'GUROBI_MIP'
    solver = pywraplp.Solver.CreateSolver(solver_name)
    solver.EnableOutput()

    # define parameters
    c = [[100, 300, 700, 400, 300], # transport costs from loc i to customer j
        [600, 400, 100, 500, 600],
        [700, 200, 100, 400, 700]]
    d = [40, 130, 110, 50, 30]      # demand customer j
    f = [110, 120, 150]             # capacity location i

    # determine index sets
    I = list(range(len(f)))
    J = list(range(len(d)))

    # define upper bound for decision variables
    X_ub = sum(d)
    # declare decision variables
    X = {}
    for i in I:
        for j in J:
            X[(i, j)] = solver.IntVar(0.0, X_ub, 'task_i%ij%i' % (i, j))

    # constraint 1: Demand must be satisfied
    for j in J:
        solver.Add(sum(X[(i, j)] for i in I) >= d[j])

    # constraint 2: Capacity must not be exceeded
    for i in I:
        solver.Add(sum(X[(i, j)] for j in J) <= f[i])

    # objective function
    solver.Minimize(sum(X[(i, j)] * c[i][j] for i in I for j in J))
    # solve the model
    status = solver.Solve()

    if status == pywraplp.Solver.OPTIMAL:
        print("Solution:")
        print("Objective value =", solver.Objective().Value())
        for i in I:
            for j in J:
                print("X_{}_{} = {}".format(i, j, X[(i, j)].solution_value()))
    else:
        print("The problem does not have an optimal solution.")


if __name__ == "__main__":
    main()