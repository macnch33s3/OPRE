import networkx as nx
import matplotlib.pyplot as plt

def main():
    # Create a directed graph object
    g = nx.DiGraph()

    # Add edges to the graph based on the adjacency list
    g.add_edges_from([("A", "B"), ("B", "C"), ("C", "A")])

    # Define the graph layout
    pos = nx.spring_layout(g)

    # Draw nodes and edges of the graph
    nx.draw(g, pos, with_labels=True, node_size=500, node_color="skyblue", font_size=10, font_weight='bold', arrows=True)
    
    # Display the graph
    plt.show()

    print("Graph g is {}".format("directed" if g.is_directed() else "undirected"))

if __name__ == "__main__":
    main()
    