def read_subsetsum_problem(file_name):
    """
    reads a subset sum problem instance in a given file and
    returns the items as well as the limit capacity

    :param file_name: the subset sum instance filename
    :return: a list with weights, in addition the limit capacity which has to be reached
    :return: dictionary with item-id as key, weight as value, in addition the capacity limit as a separate value
    """
    items = {}
    limit_capacity = 0
    num_items = 0

    with open(file_name, "r") as file:
        lines = file.readlines()
        for line in lines:
            if line.startswith("NUM_ITEMS"):
                num_items = int(line.split(":")[1].strip())
            elif line.startswith("LIMIT_CAPACITY"):
                limit_capacity = float(line.split(":")[1].strip())
            elif line.startswith("ITEMS_ID_WEIGHT"):
                item_start_index = lines.index(line) + 1
                for item_line in lines[item_start_index:item_start_index + num_items]:
                    item_id, weight = item_line.split()
                    items[int(item_id)] = float(weight)
                break

    return items, limit_capacity
