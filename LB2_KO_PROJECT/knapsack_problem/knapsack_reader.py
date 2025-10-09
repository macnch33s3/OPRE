import pytest


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


# *******************************************************************************************************************
#  Testcases to validate if code is working as expected       
#  Run with: 'pytest -v .\LB2_KO_PROJECT\knapsack_problem\KNAPSACK_READER.py'
# *******************************************************************************************************************
def test_read_knapsack_problem():
    """
    test, whether the reader method for the knapsack problem returns the expected values / data.

    :return:
    """
    file_path = './data/CAP_KS_5.ks'
    # read problem instance
    items, capacity = read_knapsack_problem(file_path)
    # make sure, datatype of items-variable is dict
    assert type(items) == dict, "Expected items to be of type dict, but failed."
    # make sure, the dict contains 5 entries
    assert len(items) == 5, "Expected to find 5 items in dict items, but found " + str(len(items))
    # make sure the capacity contains the expected value
    assert capacity == 15, "Expected capacity to be 15 but got " + str(capacity)