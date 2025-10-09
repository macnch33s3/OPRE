import networkx as nx
import matplotlib.pyplot as plt

def main():
    # generate an (undirected) graph object
    g = nx.Graph()

    # add multiple edges from adjacency list
    g.add_edges_from([(1, 2), (1, 3), (2, 3), (2, 4), (3, 4), (4, 5)])

    # Node coloring with a greedy algorithm
    node_colors = nx.coloring.greedy_color(g, strategy="largest_first")

    # Color palette for visualization
    color_map = [node_colors[node] for node in g.nodes()]

    # Drawing  colored nodes and edges of the graph
    pos = nx.spring_layout(g, seed=42)
    nx.draw(g, pos, with_labels=True, node_color=color_map, cmap=plt.cm.rainbow)
    plt.show()

if __name__ == "__main__":
    main()