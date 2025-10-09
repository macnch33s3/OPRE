def read_1dbinpacking_file(file_path):
    """
    reads a 1d binpacking problem instance

    :param file_path: the file path
    :return: dictionary with item-id as key, dimension as value, in addition the capacity limit as a separate value
    """
    with open(file_path, 'r') as file:
        lines = file.readlines()

    container_cap = None
    items = {}

    for line in lines:
        line = line.strip()

        # Skip empty lines and the header lines
        if not line or line.startswith("NAME") or line.startswith("TYPE") or line.startswith("COMMENT"):
            continue

        # Extract container capacity
        if line.startswith("CONTAINER_CAP"):
            container_cap = float(line.split(":")[1].strip())
            continue

        # Extract item dimensions (after "OBJ_ID_DIM" line)
        if line[0].isdigit():
            item_id, item_dim = line.split()
            items[int(item_id)] = float(item_dim)

        # Stop reading if "EOF" is reached
        if line == "EOF":
            break

    return items, container_cap