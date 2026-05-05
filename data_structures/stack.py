from typing import Any

# LIFO — Last In, First Out
# push
# pop
# peek
# is_empty


def create_stack() -> list:
    """Create an empty stack"""
    return []


def is_empty(stack: list) -> bool:
    """Check if stack is empty"""
    return len(stack) == 0


def push(stack: list, item: Any) -> None:
    """Push item into stack"""
    stack.append(item)

def pop(stack: list) -> Any:
    """Remove the item at the top of the stack"""
    if not is_empty(stack):
        return stack.pop()
    else:
        print("Stack is empty")
        return []

def peek(stack: list) -> Any:
    """Show the item at the top of the stack"""
    if not is_empty(stack):
        return stack[-1]
    else:
        print("Stack is empty")
        return []


stack = create_stack()
push(stack, 'a')
push(stack, 'b')
push(stack, 'c')
print(peek(stack))  # Output: 'c'
print(pop(stack))   # Output: 'c'
print(peek(stack))  # Output: 'b'