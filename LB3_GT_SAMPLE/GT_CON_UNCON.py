import networkx as nx
import matplotlib.pyplot as plt

def main():
    # Create a graph
    g = nx.Graph()

    # Add nodes
    nodes = [1, 2, 3]
    g.add_nodes_from(nodes)

    # Add edges
    edges = [(1, 2)]
    g.add_edges_from(edges)

    # Creating the layout for the graph visualization
    pos = nx.spring_layout(g, seed=2)

    # Drawing nodes and edges of the graph
    nx.draw(g, pos, with_labels=True, node_size=500)
    # Display the graph
    plt.show()

    # Check if the graph is connected
    is_connected = nx.is_connected(g)

    if is_connected:
        print("The graph is connected.")
    else:
        print("The graph is not connected.")

if __name__ == "__main__":
    main()
    