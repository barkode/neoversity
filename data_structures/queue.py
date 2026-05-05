from collections import deque

# FIFO — First In, First Out

# Enqueue - add element at the end
# Dequeue - delete element from begin
# Front / Peek - show the first element
# Is Empty - check if queue is empty
# Size - show quantity of queue elements

queue = deque()

# Enqueue
queue.append('a')
queue.append('b')
queue.append('c')
queue.append('d')

print("Enqueue: ", list(queue))

# Dequeue
print("Dequeue: ", queue.popleft())
print("Queue after Dequeue: ", list(queue))

# Peek
print("Peek :", queue[0])

# Is Empty
print("IS EMPTY: ", len(queue) == 0)

# SIZE
print('SIZE: ', len(queue))