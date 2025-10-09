import numpy as np

def read_flp_file(file_path):
    """
    Reads a Facility Location Problem (FLP) file and extracts the depot costs and distance matrix.

    :param file_path: the facility location problem instance filename
    :return: a list of costs for each depot, the depot / unit distance matrix
    """
    crit_dist = None
    depot_costs = []
    distance_matrix = []
    reading_costs = False
    reading_matrix = False

    with open(file_path, 'r') as file:
        lines = file.readlines()

    for line in lines:
        if line.startswith("NUM_DEPOTS"):
            num_depots = int(line.split(":")[1].strip())
        elif line.startswith("NUM_UNITS"):
            num_units = int(line.split(":")[1].strip())
        elif line.startswith("CRITICAL_DISTANCE"):
            crit_dist = float(line.split(":")[1].strip())
        elif line.startswith("DEPOT_COST"):
            reading_costs = True
            reading_matrix = False
        elif line.startswith("DEPOT_UNIT_DISTANCE_MATRIX"):
            reading_costs = False
            reading_matrix = True
        elif line.startswith("EOF"):
            break
        elif reading_costs:
            parts = line.split()
            depot_costs.append(float(parts[1]))
        elif reading_matrix:
            parts = line.split()
            distances = list(map(float, parts[1].split(";")))
            distance_matrix.append(distances)

    # convert datatypes from lists to np-arrays for more efficient math
    depot_costs = np.array(depot_costs)
    distance_matrix = np.array(distance_matrix, dtype=float)

    # Now validate num_depots / num_units numbers indicated with data provided
    assert num_depots == len(depot_costs), "Number of depots does not match dimension of depot cost list."
    assert num_units == distance_matrix.shape[1], "Number of units does not match number of rows in distance matrix."
    assert crit_dist is not None, "Expected critical distance to be defined but nothing found."

    return crit_dist, depot_costs, distance_matrix
