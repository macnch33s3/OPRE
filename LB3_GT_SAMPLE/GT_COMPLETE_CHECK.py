import networkx as nx

def is_complete_graph(graph):
    num_nodes = len(graph.nodes)
    num_edges = len(graph.edges)
    max_edges = num_nodes * (num_nodes - 1) // 2
    return num_edges == max_edges

def main():
    # Example: Create a complete graph with 4 nodes
    first_graph = nx.complete_graph(4)

    # Example: Create a graph with 4 nodes that is not a complete graph
    second_graph = nx.Graph()
    second_graph.add_nodes_from([1, 2, 3, 4])
    second_graph.add_edges_from([(1, 2), (2, 3), (3, 4)])

    print("Is the first graph a complete graph?", is_complete_graph(first_graph))
    print("Is the second graph a complete graph?", is_complete_graph(second_graph))

if __name__ == "__main__":
    main()  
