from ortools.linear_solver import pywraplp

def main():
    	# UMP23: Kursplanung (Timon Grütter)
	# Create the model.
	# solver_name = 'SCIP'  # alternatively: 'GUROBI_MIP'
	solver_name = 'CP-SAT'  # alternatively: 'GUROBI_MIP'
	solver = pywraplp.Solver.CreateSolver(solver_name)
	solver.EnableOutput()

	# define parameters
	t = [5, 2, 3, 4, 3, 5, 3, 4, 5, 3]
	e = [500, 2500, 6000, 10000, 5800, 7500, 6000, 4800, 10000, 10000]
	a = [750, 200, 300, 1200, 300, 500, 600, 200, 1000, 1200]
	w = [0, 1, 1, 1, 1, 0, 1, 0, 0, 1]

	# determine index sets
	I = list(range(len(t)))

	# declare decision variables
	X = {}
	for i in I:
		X[i] = solver.BoolVar('Entscheidungsvar_i%i' % i)

	# constraint 1: nicht mehr als 20 Tage
	for i in I:
		solver.Add(sum(X[i] * t[i] for i in I) <= 20)

	# constraint 2: nicht mehr als 4 WEs
	for i in I:
		solver.Add(sum(X[i] * w[i] for i in I) <= 4)

	# constraint 3: Veranstaltung 4 und 9 nicht beide
	solver.Add(X[3] + X[8] <= 1)

	# objective function
	solver.Maximize(sum(X[i] * (e[i] - a[i]) for i in I))
	# solve the model
	status = solver.Solve()

	if status == pywraplp.Solver.OPTIMAL:
		print("Solution:")
		print("Objective value =", solver.Objective().Value())
		for i in I:
			print("X_{} = {}".format(i, X[i].solution_value()))

	else:
		print("The problem does not have an optimal solution.")


if __name__ == "__main__":
    main()
	