# Samplescript mit MILP + Google OR-Tools für einfaches capacitated Knapsack-Problem

import numpy as np
from ortools.linear_solver import pywraplp


def read_knapsack_problem(file_name):
    """
    reads a capacitated knapsack problem instance in a given file and
    returns the items as well as the knapsack capacity

    :param file_name: the knapsack instance filename
    :return: dictionary with item-id as key, tuple with (weight, value)
             as value, in addition the knapsack capacity as a separate
             value
    """
    items = {}
    knapsack_capacity = 0
    num_items = 0

    with open(file_name, "r") as file:
        lines = file.readlines()
        for line in lines:
            if line.startswith("NUM_ITEMS"):
                num_items = int(line.split(":")[1].strip())
            elif line.startswith("KNAPSACK_CAPACITY"):
                knapsack_capacity = float(line.split(":")[1].strip())
            elif line.startswith("ITEMS_ID_WEIGHT_VALUE"):
                item_start_index = lines.index(line) + 1
                for item_line in lines[item_start_index:item_start_index + num_items]:
                    item_id, weight, value = item_line.split()
                    items[int(item_id)] = (float(weight), float(value))
                break

    return items, knapsack_capacity


def convert_1d_var(var, size):
    """
    Konvertiert die 1d Google OR-Tools Solution-Variable var in eine brauchbare Variable

    :param var: Google OR-Tools 1d-solution Variable
    :param size: dimension of the 1d-variable
    """
    retval = np.zeros(shape=size, dtype=np.int8)
    for k in range(0, size):
        retval[k] = var[k].solution_value()
    return retval.tolist()


def solve_knapsack_milp(items, capacity):
    # Init return values
    solution = []
    weight = 0.0
    value = 0.0

    # Create the model.
    solver_name = 'CP-SAT'  # use this for satisfiability or plain INT MILP models
    # solver_name = 'SCIP'  # use this, if MILP cannot be transformed to INT
    # solver_name = 'GUROBI_MIP'  # use & pay this, if nothing else helps/time is critical
    solver = pywraplp.Solver.CreateSolver(solver_name)
    # solver.EnableOutput()

    # define parameters
    w = [item[0] for item in items.values()]
    v = [item[1] for item in items.values()]

    # define index sets
    I = range(len(items))

    # declare decision variables
    X = {}
    for i in I:
        X[i] = solver.BoolVar('item_i%i' % i)

    # constraint 1: Capacity must not be exceeded
    solver.Add(sum(X[i] * w[i] for i in I) <= capacity)

    # objective function
    solver.Maximize(sum(X[i] * v[i] for i in I))
    # solve the model
    status = solver.Solve()

    if status == pywraplp.Solver.OPTIMAL:
        solution = convert_1d_var(X, len(items))
        value = sum(solution[i] * v[i] for i in I)
        weight = sum(solution[i] * w[i] for i in I)
        print("Optimal solution found.")
    else:
        print("The problem does not have an optimal solution.")
    return solution, weight, value


# *******************************************************************************************************************
# * Main Program                                                                                                    *
# *******************************************************************************************************************
def main():
    file_paths = ['./data/CAP_KS_3.ks', './data/CAP_KS_5.ks', './data/CAP_KS_8.ks',
                  './data/CAP_KS_48.ks', './data/CAP_KS_140.ks', './data/CAP_KS_2844.ks']

    for file in file_paths:
        # Read the problem instance
        items, knapsack_capacity = read_knapsack_problem(file)
        # Create a first solution applying a primitive k-heuristic
        print(f"*** File {file}:")
        solution, weight, value = solve_knapsack_milp(items, knapsack_capacity)
        index_list = [i + 1 for i in range(len(items)) if solution[i] == 1]
        print(f"Num Items: {len(items)}")
        print(f"Capacity: {knapsack_capacity}")
        # print(f"Solution: {', '.join(map(str, index_list[:5]))}{'...' if len(index_list) > 5 else ''}")
        print(f"Solution: {', '.join(map(str, index_list))}")
        print(f"Total Weight: {round(weight, 2)}")
        print(f"Total Value: {round(value, 2)}")


if __name__ == "__main__":
    main()
