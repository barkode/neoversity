import heapq

import networkx as nx
import matplotlib.pyplot as plt


#TODO Створення власного вагового графа (Наданий приклад не підходить для перевірки роботи алгоритму)
G = nx.Graph()
G.add_edge("A", "B", weight=1)
G.add_edge("B", "C", weight=2)
G.add_edge("C", "D", weight=3)

# Реалізація алгоритму Дейкстри
def dijkstra(graph, start):
    shortest_paths = {vertex: float('infinity') for vertex in graph}
    shortest_paths[start] = 0
    priority_queue = [(0, start)]
    while priority_queue:
        #TODO Реалізація алгоритму Дейкстри використовуючи бінарну купу
        pass
    return shortest_paths


# Використання алгоритму Дейкстри
shortest_paths = dijkstra(G, "A")
print(shortest_paths)

# Візуалізація графа
pos = nx.spring_layout(G)  # Positions for all nodes
nx.draw_networkx_nodes(G, pos, node_size=700)
nx.draw_networkx_edges(G, pos, width=2)
edge_labels = nx.get_edge_attributes(G, 'weight')
nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)
nx.draw_networkx_labels(G, pos, font_size=20, font_family="sans-serif")

plt.axis("off")
plt.show()
