from collections import deque

# Tasks list

tasks = [
    {"type": "fast", "name": "Do the dishes"},
    {"type": "slow", "name": "Watch tv show"},
    {"type": "fast", "name": "Walk the dog"},
    {"type": "slow", "name": "Read a book"},
    {"type": "fast", "name": "Go to the gym"},
    {"type": "slow", "name": "Cook dinner"},
    {"type": "fast", "name": "Clean the house"},
    {"type": "slow", "name": "Do laundry"},
    {"type": "fast", "name": "Go grocery shopping"},
    {"type": "slow", "name": "Write a blog post"},
    ]

# Tasks initialization
task_queue = deque()

# Allocation of tasks into a queue according to their priority
for task in tasks:
    if task["type"] == "fast":
        task_queue.appendleft(task)  # High priority
        print(f"Adding high priority task {task['name']}")
    else:
        task_queue.append(task)  # Low priority
        print(f"Adding low priority task {task['name']}")

print(task_queue)

# Task completion
while task_queue:
    task = task_queue.popleft()
    print(f"Completed task {task['name']} - {task['type']}")
