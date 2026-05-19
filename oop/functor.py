# __call__,

class Multiplier:
    def __init__(self, factor):
        self.factor = factor

    def __call__(self, other):
        return self.factor * other


# Створення екземпляра функтора
double = Multiplier(2)
triple = Multiplier(3)

# Виклик функтора
print(double(5))  # Виведе: 10
print(triple(3))  # Виведе: 9


class Counter:
    def __init__(self):
        self.count = 0

    def __call__(self, *args, **kwargs):
        self.count += 1


counter = Counter()
counter()
counter()
print(f"Викликано {counter.count} разів")


class SmartCalculator:
    def __init__(self, operation='add'):
        self.operation = operation

    def __call__(self, a, b):
        if self.operation == 'add':
            return a + b
        elif self.operation == 'subtract':
            return a - b
        else:
            raise ValueError("Невідома операція")


add = SmartCalculator('add')
print(add(5, 3))  # 8

subtract = SmartCalculator('subtract')
print(subtract(10, 7))  # 3
