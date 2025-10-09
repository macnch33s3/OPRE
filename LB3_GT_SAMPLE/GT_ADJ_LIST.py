import matplotlib.pyplot as plt
import networkx as nx

# Reference: https://networkx.org/documentation/stable/tutorial.html

def main():
    # generate an (undirected) graph object
    g = nx.Graph()

    # add multiple edges from adjacency list
    g.add_edges_from([(6,4), (4,3), (4,5), (3,2), (5,2), (5,1), (2,1) ])

    # define the graph layout
    pos = nx.spring_layout(g, seed=3068)  # Seed layout for reproducibility
    # prepare the graph drawing in memory
    nx.draw(g, pos=pos, with_labels=True)
    # output the graph
    plt.show()

if __name__ == "__main__":
    main()