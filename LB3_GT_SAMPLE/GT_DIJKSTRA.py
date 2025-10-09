import networkx as nx
import matplotlib.pyplot as plt

def main():
    # Create a weighted graph
    G = nx.Graph()

    # Add nodes
    G.add_nodes_from([1, 2, 3, 4, 5])

    # Add weighted edges
    G.add_edge(1, 2, weight=4)
    G.add_edge(1, 3, weight=2)
    G.add_edge(2, 3, weight=5)
    G.add_edge(2, 4, weight=10)
    G.add_edge(3, 5, weight=1)
    G.add_edge(4, 5, weight=6)

    # Create a layout for the graph visualization
    pos = nx.spring_layout(G, seed=4)

    # Visualize the graph with edge weights
    plt.figure(figsize=(8, 6))
    nx.draw(G, pos, with_labels=True, font_weight='bold', node_color='lightblue', edge_color='gray', width=2, node_size=500)
    edge_labels = {(u, v): data['weight'] for u, v, data in G.edges(data=True)}
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)
    plt.show()

    # Specify the start node for Dijkstra's algorithm
    start_node = 1

    # Find the shortest paths and distances using Dijkstra's algorithm
    shortest_paths = nx.single_source_dijkstra_path(G, start_node, weight='weight')
    shortest_distances = nx.single_source_dijkstra_path_length(G, start_node, weight='weight')

    # Print the distances and costs of all nodes from the start node
    print("Shortest distances and costs from node", start_node, "to all other nodes:")
    for node in sorted(G.nodes()):
        path = shortest_paths[node]
        cost = shortest_distances[node]
        print(f"Node {node} - Path: {path} - Cost: {cost}")


if __name__ == "__main__":
    main()
    