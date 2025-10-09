# Samplescript with k-heuristic with rnd LS for simple capacitated Knapsack Problem
import numpy as np


def read_knapsack_problem(file_name):
    """
    Reads a capacitated knapsack problem instance from a specified file
    and returns the items along with the knapsack capacity.

    :param file_name: The name of the file containing the knapsack instance.
    :return: A tuple containing:
             - A dictionary with item IDs as keys and tuples of (weight, value) as values.
             - The knapsack capacity as a separate float value.
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


def knapsack_greedy(items, capacity):
    """
    Implements a greedy approach to solve the knapsack problem.

    :param items: A dictionary with item_id as key and a tuple of (weight, value) as value.
    :param capacity: The maximum capacity of the knapsack.
    :return: A tuple containing:
             - A binary list indicating which items have been selected.
             - The total weight of the selected items.
             - The total value of the selected items.
    """
    # Sort items in descending order based on value/weight ratio
    sorted_items = sorted(items.items(), key=lambda x: x[1][1] / x[1][0], reverse=True)

    # Initialize total weight, total value, and the selection array
    total_weight = 0
    total_value = 0
    selected_binary = [0] * (max(items.keys()))

    # Select items based on the greedy approach
    for item_id, (weight, value) in sorted_items:
        if total_weight + weight <= capacity:
            selected_binary[item_id - 1] = 1
            total_weight += weight
            total_value += value
        else:
            continue

    return selected_binary, total_weight, total_value


def evaluate_solution(solution, items):
    """
    Helper function to compute the total weight and value of a given solution.

    :param solution: A binary list indicating the inclusion of items in the solution.
    :param items: A dictionary containing item information (weight, value).
    :return: A tuple containing:
             - The total weight of the solution.
             - The total value of the solution.
    """
    weights, values = zip(*items.values())
    total_weight = np.dot(np.array(weights), np.array(solution))
    total_value = np.dot(np.array(values), np.array(solution))
    return total_weight, total_value


def generate_neighbors(solution):
    """
    Generates all neighbors by inserting, deleting, and swapping items.

    :param solution: A binary list indicating the current solution.
    :return: A list of neighbor solutions.
    """
    neighbors = []
    n = len(solution)

    # Insert: Add an item (if it is not already included)
    for i in range(n):
        if solution[i] == 0:  # Only insert if the item is not included
            new_solution = solution[:]
            new_solution[i] = 1
            neighbors.append(new_solution)

    # Delete: Remove an item (if it is already included)
    for i in range(n):
        if solution[i] == 1:  # Only remove if the item is included
            new_solution = solution[:]
            new_solution[i] = 0
            neighbors.append(new_solution)

    # Swap: Remove one item and add another
    for i in range(n):
        if solution[i] == 1:  # Remove an item
            for j in range(n):
                if solution[j] == 0:  # Add another item
                    new_solution = solution[:]
                    new_solution[i] = 0
                    new_solution[j] = 1
                    neighbors.append(new_solution)

    return neighbors


def knapsack_local_search(items, capacity, initial_solution, weight, value):
    """
    Performs local search to improve the initial solution for the knapsack problem.

    :param items: A dictionary with item information (weight, value).
    :param capacity: The maximum capacity of the knapsack.
    :param initial_solution: The initial binary list representing the solution.
    :param weight: The total weight of the initial solution.
    :param value: The total value of the initial solution.
    :return: A tuple containing:
             - The best solution found.
             - The total weight of the best solution.
             - The total value of the best solution.
    """
    # Initialize the best solution
    best_solution = initial_solution[:]
    best_weight = weight
    best_value = value

    improved = True
    while improved:
        improved = False
        neighbors = generate_neighbors(best_solution)

        for neighbor in neighbors:
            neighbor_weight, neighbor_value = evaluate_solution(neighbor, items)

            # Check if the neighbor is better and does not exceed capacity
            if neighbor_value > best_value and neighbor_weight <= capacity:
                best_solution = neighbor[:]
                best_weight = neighbor_weight
                best_value = neighbor_value
                improved = True

    return best_solution, best_weight, best_value


def generate_random_solution(items, knapsack_capacity):
    """
    Generates a random feasible solution for the knapsack problem.

    :param items: 
        A dictionary where each key is an item ID, and each value is a tuple (weight, value).
    :param knapsack_capacity: 
        The maximum capacity of the knapsack.

    :return: 
        A tuple containing:

        - **solution** (*list of int*): A binary list (0s and 1s) representing a random selection of items.
        - **total_weight** (*int*): The total weight of the selected items.
        - **total_value** (*int*): The total value of the selected items.

    :rtype: tuple (list, int, int)
    """  # Extract weights and values from the items dictionary into separate lists
    weights, values = zip(*items.values())

    n = len(items)

    while True:
        # Generate a random binary vector (0 or 1 for each item)
        solution = np.random.randint(2, size=n)

        # Calculate the total weight of the selected items via matrix multiplication
        total_weight = np.dot(np.array(weights), np.array(solution))
        total_value = np.dot(np.array(values), np.array(solution))

        # Check if the total weight is within the knapsack capacity limit
        if total_weight <= knapsack_capacity:
            return solution.tolist(), total_weight, total_value


def knapsack_randomized_local_search(items, capacity):
    """
     Perform a randomized local search to solve the 0/1 knapsack problem.

     The function attempts to find the optimal combination of items that fits within the given
     capacity of the knapsack while maximizing the total value. It uses a randomized local search
     approach, where random solutions are generated, evaluated, and neighbors are explored to find
     better solutions. The search continues until a maximum number of failed attempts (non-improving
     iterations) is reached.

     :param items: List of tuples representing the items. Each tuple contains (weight, value).
     :type items: list[tuple[int, int]]
     :param capacity: Maximum weight capacity of the knapsack.
     :type capacity: int
     :return: A tuple containing the best solution (list of selected items), the total weight of the solution, and its total value.
     :rtype: tuple[list[bool], int, int]
     """
    # Initialize variables to store the best solution found
    best_solution, best_weight, best_value = knapsack_greedy(items, capacity)

    # Initialize the number of failed attempts and the maximum allowed failed attempts
    cnt = 0
    best_value = 0

    while cnt < 30:
        # Generate a random solution and evaluate its weight and value
        solution, weight, value = generate_random_solution(items, capacity)
        # trigger local search from solution
        solution, weight, value = knapsack_local_search(items, capacity, solution, weight, value)
        if value > best_value:
            best_solution, best_weight, best_value = solution, weight, value
        cnt += 1

    return best_solution, best_weight, best_value


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
        print(f"*** Solving Knapsack Instance File {file} ***")
        solution, weight, value = knapsack_greedy(items, knapsack_capacity)
        index_list = [i + 1 for i in range(len(items)) if solution[i] == 1]
        print(f"Num Items: {len(items)}")
        print(f"Capacity: {knapsack_capacity}")
        print(f"Solution: {', '.join(map(str, index_list))}")
        print(f"Total Weight: {round(weight, 2)}")
        print(f"Total Value: {round(value, 2)}")
        # now improve initial solution applying a best-improvement local-search
        print(f"*** Improving solution with local search [from KH] ***")
        solution, weight, value = knapsack_local_search(items, knapsack_capacity, solution, weight, value)
        index_list = [i + 1 for i in range(len(items)) if solution[i] == 1]
        print(f"Solution: {', '.join(map(str, index_list))}")
        print(f"Total Weight: {round(weight, 2)}")
        print(f"Total Value: {round(value, 2)}")
        print(f"*** Improving solution with local search [from Empty Knapsack]***")
        solution = [0] * len(items)
        solution, weight, value = knapsack_local_search(items, knapsack_capacity, solution, 0, 0)
        index_list = [i + 1 for i in range(len(items)) if solution[i] == 1]
        print(f"Solution: {', '.join(map(str, index_list))}")
        print(f"Total Weight: {round(weight, 2)}")
        print(f"Total Value: {round(value, 2)}")
        print(f"*** Improving solution with randomized local search ***")
        solution, weight, value = knapsack_randomized_local_search(items, knapsack_capacity)
        index_list = [i + 1 for i in range(len(items)) if solution[i] == 1]
        print(f"Solution: {', '.join(map(str, index_list))}")
        print(f"Total Weight: {round(weight, 2)}")
        print(f"Total Value: {round(value, 2)}")


if __name__ == "__main__":
    main()
