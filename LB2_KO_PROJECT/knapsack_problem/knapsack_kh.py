# Samplescript mit k-Heuistik für einfaches capacitated Knapsack-Problem

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


def knapsack_greedy(items, capacity):
    """
    Packs the knapsack based on a greedy approach.

    :param items: A dictionary with item_id as key and a tuple of (weight, value) as value.
    :param capacity: The knapsack capacity.
    :return: A binary array indicating which items have been selected;
             total_weight the total weight of the Knapsack;
             total_value the total value of the Knapsack
    """
    # Sort the items in descending order by value/weight ratio
    sorted_items = sorted(items.items(), key=lambda x: x[1][1] / x[1][0], reverse=True)

    # Initialize the current total weight and the binary array
    total_weight = 0
    total_value = 0
    selected_binary = [0] * (max(items.keys()))

    # Select the items based on the greedy approach
    for item_id, (weight, value) in sorted_items:
        if total_weight + weight <= capacity:
            selected_binary[item_id - 1] = 1
            total_weight += weight
            total_value += value
        else:
            continue

    return selected_binary, total_weight, total_value


# *******************************************************************************************************************
# * Main Program                                                                                                    *
# *******************************************************************************************************************
def main():
    file_paths = ['./data/CAP_KS_3.ks', './data/CAP_KS_5.ks', './data/CAP_KS_8.ks', './data/CAP_KS_48.ks',
                  './data/CAP_KS_140.ks', './data/CAP_KS_2844.ks']

    for file in file_paths:
        # Read the problem instance
        items, knapsack_capacity = read_knapsack_problem(file)
        # Create a first solution applying a primitive k-heuristic
        solution, weight, value = knapsack_greedy(items, knapsack_capacity)

        print(f"*** File {file}:")
        print(f"Num Items: {len(items)}")
        print(f"Capacity: {knapsack_capacity}")
        # print(f"Solution: {', '.join(map(str, solution[:8]))}{'...' if len(solution) > 8 else ''}")
        print("Solution:", [i + 1 for i, value in enumerate(solution) if value == 1])
        print(f"Total Weight: {round(weight, 2)}")
        print(f"Total Value: {round(value, 2)}")


if __name__ == "__main__":
    main()
