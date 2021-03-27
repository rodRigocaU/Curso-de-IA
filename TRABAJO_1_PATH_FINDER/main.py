import networkx as nx
import matplotlib.pyplot as plt
G = nx.DiGraph()
G.add_edges_from(
    [('A', 'B'), ('A', 'C'), ('A', 'D'), ('E', 'D'), ('D', 'F'), ('E', 'C'), ('E', 'G'), ('B', 'H'), ('H', 'F')])


pos = nx.spring_layout(G)
nx.draw_networkx(G, pos)
plt.grid()
plt.show()