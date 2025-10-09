def read_2dbinpacking_file(file_path):
    """
    reads a 2d binpacking problem instance

    :param file_path: the file path
    :return: 1) dictionary with item-id as key, x-dim, y-dim and number of items as values
             2) tuple with container x-dimension and y-dimension
    
    """
    with open(file_path, 'r') as file:
        lines = file.readlines()

    container_dims = None
    items = {}

    for line in lines:
        line = line.strip()

        # Skip empty lines and the header lines
        if not line or line.startswith("NAME") or line.startswith("TYPE") or line.startswith("COMMENT"):
            continue

        # Extract container x-dimension
        if line.startswith("CONTAINER_XDIM"):
            container_xdim = float(line.split(":")[1].strip())
            continue

         # Extract container y-dimension
        if line.startswith("CONTAINER_YDIM"):
            container_ydim = float(line.split(":")[1].strip())
            container_dims = (container_xdim, container_ydim)
            continue


        # Extract item dimensions (after "OBJTYPE_ID_XDIM_YDIM_NUM" line)
        if line[0].isdigit():
            item_id, item_xdim, item_ydim, item_num = line.split()
            items[int(item_id)] = (float(item_xdim), float(item_ydim), int(item_num))


        # Stop reading if "EOF" is reached
        if line == "EOF":
            break

    return items, container_dims




if __name__ == "__main__":
    items, container_cap = read_2dbinpacking_file("bin_packing_2d/data/BIN_PACK_2D_C10X10_O28.bpk")
    print(f"Container capacity: {container_cap}")
    print(f"Items: {items}")