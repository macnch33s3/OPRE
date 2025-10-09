def read_tsp_file(file_path):
    """
    read TSPlib input file and return a nodes-dictionary

    :param file_path:
    :return: dict containing nodes with tupels representing x, y coordinates
    """
    nodes = {}
    with open(file_path, 'r') as file:
        lines = file.readlines()

        node_section = False
        for line in lines:
            line = line.strip()
            if line.startswith("NODE_COORD_SECTION"):
                node_section = True
                continue
            if line.startswith("EOF"):
                break
            if node_section:
                parts = line.split()
                if len(parts) == 3:
                    node_id, x, y = parts
                    nodes[int(node_id)] = (float(x), float(y))

    return nodes
