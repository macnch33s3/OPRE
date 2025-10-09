from ortools.linear_solver import pywraplp

def main():
	# Create the model.
	solver_name = 'SCIP' # alternatively: 'GUROBI_MIP'
	solver = pywraplp.Solver.CreateSolver(solver_name)
	solver.EnableOutput()

	# define parameters
	c = [[ 1, 1, 0, 0, 0, 0], # if fire truck in location i can reach locatin j
		 [ 1, 1, 0, 0, 0, 1],
		 [ 0, 0, 1, 1, 0, 0],
		 [ 0, 0, 1, 1, 1, 0],
		 [ 0, 0, 0, 1, 1, 1],
		 [ 0, 1, 0, 0, 1, 1]]

	# determine index sets
	I = list(range(len(c))) # all villages
	J = list(range(len(c))) # all villages

	# declare decision variables
	X = {}
	for i in I:
		X[i] = solver.BoolVar('village_i%i' % i)

	# constraint 1: Each village must be reachable by at least one fire truck stationed in any village
	for j in J:
		solver.Add(sum(c[i][j] * X[i] for i in I) >= 1)

	# objective function
	solver.Minimize(sum(X[i] for i in I))
	# solve the model
	status = solver.Solve()

	if status == pywraplp.Solver.OPTIMAL:
		print("Solution:")
		print("Objective value =", solver.Objective().Value())
		for i in I:
			print(f"X_{i} = {int(X[i].solution_value())}")
	else:
		print("The problem does not have an optimal solution.")


if __name__ == "__main__":
    main()
