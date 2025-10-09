import networkx as nx
import matplotlib.pyplot as plt

def main():
    # Reference: https://networkx.org/documentation/stable/tutorial.html

    # generate a complete graph of order 5
    G = nx.complete_graph(5)

    # define the graph layout
    pos = nx.spring_layout(G, seed=3)

    nx.draw(G, pos=pos, with_labels=True)
    plt.show()


if __name__ == "__main__":
    main()
    