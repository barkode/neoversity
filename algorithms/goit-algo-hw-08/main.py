import heapq


class Node:
    def __init__(self, key):
        self.left = None
        self.right = None
        self.val = key

    def __str__(self, level=0, prefix="Root: "):
        ret = "\t" * level + prefix + str(self.val) + "\n"
        if self.left:
            ret += self.left.__str__(level + 1, "L--- ")
        if self.right:
            ret += self.right.__str__(level + 1, "R--- ")
        return ret


def insert(root, key):
    if root is None:
        return Node(key)
    else:
        if key < root.val:
            root.left = insert(root.left, key)
        else:
            root.right = insert(root.right, key)
    return root


def search(root, key):
    if root is None or root.val == key:
        return root
    if key < root.val:
        return search(root.left, key)
    return search(root.right, key)


def min_value_node(node):
    current = node
    while current.left:
        current = current.left
    return current


def delete(root, key):
    if not root:
        return root
    if key < root.val:
        root.left = delete(root.left, key)
    elif key > root.val:
        root.right = delete(root.right, key)
    else:
        if not root.left:
            temp = root.right
            root = None
            return temp
        elif not root.right:
            temp = root.left
            root = None
            return temp
        root.val = min_value_node(root.right).val
        root.right = delete(root.right, root.val)
    return root


def find_min(root):
    """
    Повертає найменше значення у BST.
    Найменший елемент — крайній лівий вузол.
    """
    if root is None:
        return None
    return min_value_node(root).val


def sum_values(root):
    """Повертає суму всіх значень у BST рекурсивно."""
    if root is None:
        return 0
    return root.val + sum_values(root.left) + sum_values(root.right)


def min_cable_connection_cost(cables):
    """
    Мінімальні витрати на послідовне з'єднання кабелів по два.
    Жадібний алгоритм: щоразу з'єднуємо два найкоротші.
    """
    if len(cables) <= 1:
        return 0

    heapq.heapify(cables)
    total_cost = 0

    while len(cables) > 1:
        first = heapq.heappop(cables)
        second = heapq.heappop(cables)
        cost = first + second
        total_cost += cost
        heapq.heappush(cables, cost)

    return total_cost


root = Node(5)
for val in [3, 2, 4, 7, 6, 8]:
    root = insert(root, val)

root = delete(root, 7)
print(root)

print("Найменше значення:", find_min(root))
print("Сума всіх значень:", sum_values(root))

cables = [4, 3, 2, 6, 7, 2]
print("Мінімальні витрати на з'єднання кабелів:",
      min_cable_connection_cost(cables))
