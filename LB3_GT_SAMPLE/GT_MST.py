import networkx as nx
import matplotlib.pyplot as plt

def main():
    # Create an example graph
    G = nx.Graph()
    G.add_edge(1, 2, weight=3)
    G.add_edge(1, 3, weight=1)
    G.add_edge(2, 3, weight=4)
    G.add_edge(2, 4, weight=2)
    G.add_edge(3, 4, weight=5)
    G.add_edge(3, 5, weight=6)
    G.add_edge(4, 5, weight=7)

    # Compute the minimum spanning tree using Prim's algorithm
    min_spanning_tree = nx.minimum_spanning_tree(G, algorithm='prim')

    # Calculate the cost of the minimum spanning tree
    total_cost = sum(data['weight'] for _, _, data in min_spanning_tree.edges(data=True))

    # Create a layout for the graph visualization
    pos = nx.spring_layout(G, seed=5)

    # Visualize the original graph and the minimum spanning tree with edge weights
    plt.figure(figsize=(12, 6))

    plt.subplot(121)
    nx.draw(G, pos, with_labels=True, font_weight='bold', node_color='lightblue', edge_color='gray', width=2)
    edge_labels = {edge: G[edge[0]][edge[1]]['weight'] for edge in G.edges()}
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)
    plt.title("Original Graph")

    plt.subplot(122)
    nx.draw(min_spanning_tree, pos, with_labels=True, font_weight='bold', node_color='lightgreen', edge_color='green', width=2)
    edge_labels = {edge: min_spanning_tree[edge[0]][edge[1]]['weight'] for edge in min_spanning_tree.edges()}
    nx.draw_networkx_edge_labels(min_spanning_tree, pos, edge_labels=edge_labels)
    plt.title("Minimum Spanning Tree")

    plt.tight_layout()
    plt.show()

    # Print the cost of the minimum spanning tree
    print("Minimum Spanning Tree Cost:", total_cost)

if __name__ == "__main__":
    main()
    