import heapq
import uuid
from collections import deque

import matplotlib.pyplot as plt
import networkx as nx


class Node:
    def __init__(self, key, color="skyblue"):
        self.left = None
        self.right = None
        self.val = key
        self.color = color
        self.id = str(uuid.uuid4())


def add_edges(graph, node, pos, x=0, y=0, layer=1):
    if node is not None:
        graph.add_node(node.id, color=node.color, label=node.val)
        if node.left:
            graph.add_edge(node.id, node.left.id)
            l = x - 1 / 2 ** layer
            pos[node.left.id] = (l, y - 1)
            add_edges(graph, node.left, pos, x=l, y=y - 1, layer=layer + 1)
        if node.right:
            graph.add_edge(node.id, node.right.id)
            r = x + 1 / 2 ** layer
            pos[node.right.id] = (r, y - 1)
            add_edges(graph, node.right, pos, x=r, y=y - 1, layer=layer + 1)
    return graph


def draw_tree(tree_root, colors, title="", ax=None):
    """Малює дерево у переданий axes (subplot)"""
    tree = nx.DiGraph()
    pos = {tree_root.id: (0, 0)}
    tree = add_edges(tree, tree_root, pos)

    node_colors = [colors.get(node, 'skyblue') for node in tree.nodes()]
    labels = {node[0]: node[1]['label'] for node in tree.nodes(data=True)}

    if ax is None:
        ax = plt.gca()

    ax.set_title(title, fontsize=14, fontweight='bold')
    nx.draw(tree, pos=pos, labels=labels, arrows=False, node_size=2500,
            node_color=node_colors, ax=ax)


def build_heap_tree(heap):
    if not heap:
        return None
    nodes = [Node(value) for value in heap]
    n = len(nodes)
    for i in range(n):
        left_index = 2 * i + 1
        right_index = 2 * i + 2
        if left_index < n:
            nodes[i].left = nodes[left_index]
        if right_index < n:
            nodes[i].right = nodes[right_index]
    return nodes[0]


def generate_color(step, total_steps):
    base_color = [18, 150, 240]
    darken_factor = step / (total_steps - 1) if total_steps > 1 else 1.0
    brightness = 0.15 + 0.85 * darken_factor
    new_color = [min(255, int(c * brightness)) for c in base_color]
    return f'#{new_color[0]:02x}{new_color[1]:02x}{new_color[2]:02x}'


def dfs_visualize(root, total_steps):
    visited = set()
    stack = [root]
    colors = {}
    step = 0
    while stack:
        node = stack.pop()
        if node is not None and node.id not in visited:
            visited.add(node.id)
            colors[node.id] = generate_color(step, total_steps)
            step += 1
            if node.right is not None:
                stack.append(node.right)
            if node.left is not None:
                stack.append(node.left)
    return colors


def bfs_visualize(root, total_steps=1):
    visited = set()
    queue = deque([root])
    colors = {}
    step = 0
    while queue:
        node = queue.popleft()
        if node is not None and node.id not in visited:
            visited.add(node.id)
            colors[node.id] = generate_color(step, total_steps)
            step += 1
            if node.left is not None:
                queue.append(node.left)
            if node.right is not None:
                queue.append(node.right)
    return colors


def count_nodes(node):
    if node is None:
        return 0
    return 1 + count_nodes(node.left) + count_nodes(node.right)


if __name__ == '__main__':
    print("=" * 50)
    print("Візуалізація обходу бінарного дерева")
    print("=" * 50)

    heap_list = [1, 3, 5, 7, 9, 2, 4, 34, 2, 1, 2]
    heapq.heapify(heap_list)
    print(f"Купа: {heap_list}")

    heap_tree_root = build_heap_tree(heap_list)
    print("✓ Дерево побудовано")

    total_steps = count_nodes(heap_tree_root)
    print(f"✓ Кількість вузлів: {total_steps}")

    dfs_colors = dfs_visualize(heap_tree_root, total_steps)
    print("✓ DFS обхід обчислено")

    bfs_colors = bfs_visualize(heap_tree_root, total_steps)
    print("✓ BFS обхід обчислено")

    # Відображення обох дерев в одному вікні
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))
    fig.suptitle("Візуалізація обходу бінарного дерева", fontsize=16,
                 fontweight='bold')

    draw_tree(heap_tree_root, dfs_colors,
              title="DFS - Обхід у глибину (Стек)", ax=ax1)
    print("✓ DFS дерево намальовано")

    draw_tree(heap_tree_root, bfs_colors,
              title="BFS - Обхід у ширину (Черга)", ax=ax2)
    print("✓ BFS дерево намальовано")

    plt.tight_layout()
    plt.show()
