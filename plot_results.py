import matplotlib.pyplot as plt
import numpy as np
import networkx as nx


def plot_results(coords: np.ndarray, routes: list[list[int]]) -> None:
    G = nx.Graph()
    nodes = [i for i in range(len(coords))]
    G.add_nodes_from(nodes)
    for route in routes:
        edges = [(route[i], route[i + 1]) for i in range(len(route) - 1)]
        edges.append((route[-1], route[0]))
        G.add_edges_from(edges)

    colors = ['blue' if u in routes[0] else 'red' for u, _ in G.edges()]
    pos = {i: (coords[i][0], coords[i][1]) for i in range(len(coords))}
    plt.figure(figsize=(20, 20))
    nx.draw(G, pos=pos, edge_color=colors, with_labels=True)
    plt.show()
