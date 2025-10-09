import networkx as nx
import matplotlib.pyplot as plt

def main():
    # Create a graph
    G = nx.Graph()

    # Add nodes
    G.add_nodes_from([1, 2, 3, 4])

    # Add edges
    G.add_edges_from([(1, 2), (2, 3), (3, 4), (3, 1)])

    # Visualize the graph
    pos = nx.spring_layout(G, seed=42)  # Layout for the nodes
    nx.draw(G, pos, with_labels=True, node_size=500, font_size=10, font_color='black')
    plt.title("Simple 4-Node Graph")
    plt.show()

    # Check the degree of a specific node
    selected_node = 3
    degree = G.degree[selected_node]

    # Display the degree on the console
    print(f"The degree of node {selected_node} is: {degree}")

if __name__ == "__main__":
    main()
    