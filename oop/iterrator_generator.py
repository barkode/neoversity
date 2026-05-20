# iterator __iter()__, __next()__

class CountDown:
    def __init__(self, start):
        self.current = start

    def __iter__(self):
        return self

    def __next__(self):
        if self.current == 0:
            raise StopIteration
        self.current -= 1
        return self.current


if __name__ == '__main__':
    counter = CountDown(5)
    for count in counter:
        print(count)


# generator yield

def count_down(start):
    current = start
    current -= 1
    while current >= 0:
        yield current
        current -= 1


# Використання генератора
for count in count_down(5):
    print(count)

from random import randint


class RandIterator:
    def __init__(self, start, end, quantity):
        self.start = start
        self.end = end
        self.quantity = quantity
        self.count = 0

    def __iter__(self):
        return self

    def __next__(self):
        self.count += 1
        if self.count > self.quantity:
            raise StopIteration
        else:
            return randint(self.start, self.end)


if __name__ == '__main__':
    my_random_list = RandIterator(1, 20, 5)

    for rn in my_random_list:
        print(rn, end=' ')

from random import randint


def rand_generator(start, end, quantity):
    count = 0
    while count < quantity:
        yield randint(start, end)
        count += 1


if __name__ == '__main__':
    for rn in rand_generator(1, 20, 5):
        print(rn, end=' ')


# send() in generator

def my_generator():
    received = yield "Ready"
    yield f"Received: {received}"


gen = my_generator()
print(next(gen))  # Ready
print(gen.send("Hello"))  # Received: Hello


def my_generator():
    try:
        yield "Working"
    except GeneratorExit:
        print("Generator is being closed")


gen = my_generator()
print(next(gen))  # Отримуємо "Working"
gen.close()  # Викликаємо закриття генератора


def square_numbers():
    try:
        while True:  # Нескінченний цикл для прийняття чисел
            number = yield  # Отримання числа через send()
            square = number ** 2  # Піднесення до квадрата
            yield square  # Повернення результату
    except GeneratorExit:
        print("Generator closed")


# Створення і старт генератора
gen = square_numbers()

# Ініціалізація генератора
next(gen)  # Або gen.send(None), щоб стартувати

# Відправлення числа в генератор і отримання результату
result = gen.send(10)  # Повинно повернути 100
print(f"Square of 10: {result}")

# Перехід до наступного очікування
next(gen)

# Відправлення іншого числа
result = gen.send(5)  # Повинно повернути 25
print(f"Square of 5: {result}")

# Закриття генератора
gen.close()


#   Square of 10: 100
#   Square of 5: 25
#   Generator closed

def filter_lines(keyword):
    print(f"Looking for {keyword}")
    try:
        while True:  # Нескінченний цикл, де генератор чекає на вхідні дані
            line = yield  # Отримання рядка через send()
            if keyword in line:  # Перевірка на наявність ключового слова
                yield f"Line accepted: {line}"
            else:
                yield None
    except GeneratorExit:
        print("Generator closed")


if __name__ == "__main__":
    # Створення і старт генератора
    gen = filter_lines("hello")
    next(gen)  # Потрібно для старту генератора
    messages = ["this is a test", "hello world", "another hello world line",
                "hello again", "goodbye"]
    hello_messages = []
    # Відправлення даних у генератор
    for message in messages:
        result = gen.send(message)  # Відправляємо повідомлення в генератор
        if result:  # Додаємо результат, тільки якщо він не None
            hello_messages.append(result)
        next(gen)  # Продовжуємо до наступного yield: інструкція line = yield

    # Закриття генератора
    gen.close()
    print(hello_messages)

#   Looking for hello
#   Generator closed
#   ['Line accepted: hello world', 'Line accepted: another hello world line', 'Line accepted: hello again']
