from collections import deque

# append(x) - add x to the right side of the deque
# appendleft(x) - add x to the left side of the deque
# pop() - remove and return an element from the right side of the deque
# popleft() - remove and return an element from the left side of the deque
# extend(iterable) - extend the right side of the deque by appending elements from the iterable argument
# extendleft(iterable) - extend the left side of the deque by appending elements from the iterable argument (note that the series of left appends results in reversing the order of the elements in the iterable argument)
# rotate(n) - rotate the deque n steps to the right. If n is negative, rotate to the left.
# clear() - remove all elements from the deque
# count(x) - count the number of deque elements equal to x
# reverse() - reverse the elements of the deque in-place and then return None
# copy() - create a shallow copy of the deque

d = deque()
d.append('middle') # add 'middle' to the end of the queue
d.append('last') # add 'last' to the end of the queue
d.appendleft('first') # add 'first' to the beginning of the queue

print("Queue after appending all elements: ", list(d))
print("Delete last element: ", d.pop())
print("Delete first element: ", d.popleft())
print("Queue after removing all elements: ", list(d))

# Limit the size of dequeue

c = deque(maxlen=5)
for i in range(10):
    c.append(i)

print(c)