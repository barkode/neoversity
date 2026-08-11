class Node:
    def __init__(self, data=None):
        self.data = data
        self.next = None


class LinkedList:
    def __init__(self):
        self.head = None

    def insert_at_beginning(self, data):
        new_node = Node(data)
        new_node.next = self.head
        self.head = new_node

    def insert_at_end(self, data):
        new_node = Node(data)
        if self.head is None:
            self.head = new_node
        else:
            cur = self.head
            while cur.next:
                cur = cur.next
            cur.next = new_node

    def insert_after(self, prev_node: Node, data):
        if prev_node is None:
            print("Попереднього вузла не існує.")
            return
        new_node = Node(data)
        new_node.next = prev_node.next
        prev_node.next = new_node

    def delete_node(self, key: int):
        cur = self.head
        if cur and cur.data == key:
            self.head = cur.next
            cur = None
            return
        prev = None
        while cur and cur.data != key:
            prev = cur
            cur = cur.next
        if cur is None:
            return
        prev.next = cur.next
        cur = None

    def search_element(self, data: int) -> Node | None:
        cur = self.head
        while cur:
            if cur.data == data:
                return cur
            cur = cur.next
        return None

    def print_list(self):
        current = self.head
        while current:
            print(current.data, "-->", end="")
            current = current.next
        print('None')

    def reverse(self):
        #TODO Реалізувати метод реверсування однозв'язного списку, змінюючи посилання між вузлами
        # 1 -> 2 -> 3 => 3 -> 2 -> 1
        pass

    def merge_sort(self, head):
        #TODO Реалізуавти метод сортування для однозв'язного списку (можна і не злиттям)
        # 2 -> 1 -> 3 => 1 -> 2 -> 3
        pass

    def get_middle(self, head):
        #TODO Отримати елемент в середині однозв'язного списку. Не обов'язково
        pass

    def sorted_merge(self, a, b):
        result = None

        if a is None:
            return b
        if b is None:
            return a

        if a.data <= b.data:
            result = a
            result.next = self.sorted_merge(a.next, b)
        else:
            result = b
            result.next = self.sorted_merge(a, b.next)

        return result

    def merge_sorted_lists(self, list1, list2):
        #TODO Реалізувати метод, що об'єднує два відсортовані однозв'язні списки в один відсортований список
        # 1 -> 2
        # 1 -> 3
        # Output: 1 -> 1 -> 2 -> 3
        pass

if __name__ == '__main__':

    first_list = LinkedList()

    first_list.insert_at_beginning(5)
    first_list.insert_at_beginning(10)
    first_list.insert_at_beginning(15)
    first_list.insert_at_end(20)
    first_list.insert_at_end(25)
    print("Зв'язний список:")
    first_list.print_list()

    first_list.reverse()
    print("Зв'язний список після реверсування :")
    first_list.print_list()

    first_list.head = first_list.merge_sort(first_list.head)
    print("Зв'язний список відсортовано:")
    first_list.print_list()

    second_list = LinkedList()
    first_list.insert_at_beginning(59)
    first_list.insert_at_beginning(20)
    first_list.insert_at_beginning(35)

    first_list.merge_sorted_lists(first_list, second_list)
    print("Зв'язний список відсортовано та замерджено:")
    first_list.print_list()
