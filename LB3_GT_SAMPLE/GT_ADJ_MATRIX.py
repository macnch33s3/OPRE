import matplotlib.pyplot as plt
import networkx as nx

# Reference: https://networkx.org/documentation/stable/tutorial.html

def main():
    # Reference: https://networkx.org/documentation/stable/tutorial.html

    # Example adjacency array
    adjacency_array = [
        [0, 1, 1, 0, 0],
        [1, 0, 1, 1, 0],
        [1, 1, 0, 0, 1],
        [0, 1, 0, 0, 1],
        [0, 0, 1, 1, 0]
    ]
    G = nx.Graph()

    # adding edges to the graph based on the adjacency array
    num_nodes = len(adjacency_array)

    for i in range(num_nodes):
        for j in range(num_nodes):
            if adjacency_array[i][j] == 1:
                G.add_edge(i, j)

    # define the graph layout
    pos = nx.spring_layout(G, seed=3)
    # prepare the graph drawing in memory
    nx.draw(G, pos=pos, with_labels=True)
    # display the graph
    plt.show()

if __name__ == "__main__":
    main()