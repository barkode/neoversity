import heapq

import matplotlib.pyplot as plt
import networkx as nx

# Створення власного вагового графа (Наданий приклад не підходить для перевірки роботи алгоритму)
G = nx.Graph()
edges = [
    ("A", "B", 4),
    ("A", "C", 2),
    ("B", "C", 5),
    ("B", "D", 10),
    ("C", "E", 3),
    ("E", "D", 4),
    ("D", "F", 11),
    ("E", "F", 7),
    ("B", "F", 15),
    ]
for u, v, w in edges:
    G.add_edge(u, v, weight=w)


# Реалізація алгоритму Дейкстри з використанням бінарної купи
def dijkstra(graph, start):
    # Ініціалізація відстаней: нескінченність для всіх вершин
    shortest_paths = {vertex: float('infinity') for vertex in graph}
    shortest_paths[start] = 0
    previous_nodes = {vertex: None for vertex in graph}

    # Бінарна купа: (відстань, вершина)
    priority_queue = [(0, start)]

    while priority_queue:
        # Витягуємо вершину з найменшою відстанню (мін-купа)
        current_distance, current_vertex = heapq.heappop(priority_queue)

        # Якщо знайдена відстань більша за вже відому — пропускаємо
        if current_distance > shortest_paths[current_vertex]:
            continue

        # Перебираємо сусідів поточної вершини
        for neighbor, edge_data in graph[current_vertex].items():
            weight = edge_data.get('weight', 1)
            distance = current_distance + weight

            # Якщо знайдено коротший шлях — оновлюємо
            if distance < shortest_paths[neighbor]:
                shortest_paths[neighbor] = distance
                previous_nodes[neighbor] = current_vertex
                heapq.heappush(priority_queue, (distance, neighbor))

    return shortest_paths, previous_nodes


def reconstruct_path(previous_nodes, start, end):
    """Відновлення шляху від start до end."""
    path = []
    current = end
    while current is not None:
        path.append(current)
        current = previous_nodes[current]
    path.reverse()
    return path if path[0] == start else []


# Використання алгоритму Дейкстри від вершини "A"
start_node = "A"
shortest_paths, previous_nodes = dijkstra(G, start_node)

print(f"Найкоротші відстані від вершини '{start_node}':")
for vertex, distance in sorted(shortest_paths.items()):
    path = reconstruct_path(previous_nodes, start_node, vertex)
    print(
        f"  {start_node} → {vertex}: відстань = {distance}, шлях = {' → '.join(path)}")

# Визначення ребер найкоротших шляхів для підсвічування
shortest_edges = set()
for vertex in G.nodes:
    if previous_nodes[vertex] is not None:
        shortest_edges.add((previous_nodes[vertex], vertex))
        shortest_edges.add((vertex, previous_nodes[vertex]))

# Візуалізація графа
plt.figure(figsize=(10, 7))
pos = nx.spring_layout(G, seed=42)

# Звичайні ребра
normal_edges = [(u, v) for u, v in G.edges() if (u, v) not in shortest_edges]
nx.draw_networkx_edges(G, pos, edgelist=normal_edges, width=2,
                       edge_color="gray", alpha=0.5)

# Ребра найкоротших шляхів
highlight_edges = [(u, v) for u, v in G.edges() if (u, v) in shortest_edges]
nx.draw_networkx_edges(G, pos, edgelist=highlight_edges, width=3,
                       edge_color="red")

# Вузли
nx.draw_networkx_nodes(G, pos, node_size=700, node_color="lightblue")
nx.draw_networkx_nodes(G, pos, nodelist=[start_node], node_size=700,
                       node_color="orange")

# Підписи
nx.draw_networkx_labels(G, pos, font_size=16, font_family="sans-serif",
                        font_weight="bold")
edge_labels = nx.get_edge_attributes(G, 'weight')
nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=12)

plt.title(f"Граф з найкоротшими шляхами від '{start_node}' (червоні ребра)",
          fontsize=14)
plt.axis("off")
plt.tight_layout()
plt.show()
