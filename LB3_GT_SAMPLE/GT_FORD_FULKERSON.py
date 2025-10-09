import networkx as nx
import matplotlib.pyplot as plt

def main():
    # Create a directed graph
    G = nx.DiGraph()

    # Define names of Source / Sink Nodes
    source = 's'
    sink = 't'

    # Add edges with capacities using multiple add_edge() calls
    G.add_edge(source, 'B', capacity=3)
    G.add_edge(source, 'C', capacity=2)
    G.add_edge('B', 'D', capacity=2)
    G.add_edge('C', 'D', capacity=1)
    G.add_edge('C', 'E', capacity=3)
    G.add_edge('D', sink, capacity=3)
    G.add_edge('E', sink, capacity=2)

    # Calculate the maximum flow using built-in maximum_flow function
    flow_value, flow_dict = nx.maximum_flow(G, source, sink)

    # Visualize the graph with flow values on edges
    pos = nx.spring_layout(G, seed=42)
    nx.draw(G, pos, with_labels=True, node_size=1000, node_color='lightblue', font_size=10)
    edge_labels = {(u, v): f"{flow_dict[u][v]}/{G[u][v]['capacity']}" for u, v in G.edges()}
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=8)
    plt.show()

    print("Maximum Flow:", flow_value)

if __name__ == "__main__":
    main()