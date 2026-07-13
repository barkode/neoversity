class MyContextManager:
    def __enter__(self):
        # Ініціалізація ресурсу
        print("Enter the block")
        return self  # Може повертати об'єкт

    def __exit__(self, exc_type, exc_value, traceback):
        # Звільнення ресурсу
        # exc_type: тип винятку
        # exc_val: значення винятку
        # exc_tb: трасування стеку винятку
        print("Exit the block")
        if exc_type:
            print(f"Error detected: {exc_value}")
        # Повернення False передає виняток далі, True - поглинає виняток.
        return False


# Використання власного менеджера контексту
with MyContextManager() as my_resource:
    print("Inside the block")
    raise Exception("Something went wrong")

# Вивід:
# Enter the block
# Inside the block
# Exit the block
# Error detected: Something went wrong
# Traceback (most recent call last):
# File "E:\\WebDir\\Works\\Python\\python-help-solution\\core_course\\topic7\\ex16.py", line 19, in <module>
# raise Exception("Something went wrong")
# Exception: Something went wrong

from contextlib import contextmanager


@contextmanager
def my_context_manager():
    # Ініціалізація ресурсу
    print("Enter the block")
    try:
        yield  # Місце виконання блоку `with`
    except Exception as e:
        # Обробка винятків
        print(f"Error detected: {e}")
        # Можна ре-підняти виняток або розв'язати його тут
        raise
    finally:
        # Звільнення ресурсу
        print("Exit the block")


# Використання
with my_context_manager():
    print("Inside the block")
    # raise Exception("Something went wrong")


class FileManager:
    def __init__(self, filename, mode='w', encoding='utf-8'):
        self.file = None
        self.opened = False
        self.filename = filename
        self.mode = mode
        self.encoding = encoding

    def __enter__(self):
        self.file = open(self.filename, self.mode, encoding=self.encoding)
        self.opened = True
        print("Відкриваємо файл", self.filename)
        return self.file

    def __exit__(self, exc_type, exc_val, exc_tb):
        print("Завершення блоку with")
        if self.opened:
            print("Закриваємо файл", self.filename)
            self.file.close()
        self.opened = False
        return False


if __name__ == '__main__':
    with FileManager('new_file.txt') as f:
        f.write('Hello world!\n')
        f.write('The end\n')
# Вивід:
# Відкриваємо файл new_file.txt
# Завершення блоку with
# Закриваємо файл new_file.txt

from contextlib import contextmanager


@contextmanager
def file_manager(filename, mode='w', encoding='utf-8'):
    print("Відкриваємо файл", filename)
    file = open(filename, mode, encoding=encoding)
    try:
        yield file
    finally:
        print("Закриваємо файл", filename)
        file.close()
        print("Завершення блоку with")


if __name__ == '__main__':
    with file_manager('new_file.txt') as f:
        f.write('Hello world!\n')
        f.write('The end\n')

from contextlib import contextmanager
from datetime import datetime


@contextmanager
def managed_resource(*args, **kwargs):
    log = ''
    timestamp = datetime.now().timestamp()
    msg = f'{timestamp:<20}|{args[0]:^15}| open \n'
    log += msg
    file_handler = open(*args, **kwargs)
    try:
        yield file_handler
    finally:
        diff = datetime.now().timestamp() - timestamp
        msg = f'{timestamp:<20}|{args[0]:^15}| closed {round(diff, 6):>15}s \n'
        log += msg
        file_handler.close()
        print(log)


with managed_resource('new_file.txt', 'r') as f:
    print(f.read())

# Hello world!
# The end
#
# 1707565076.245372 | new_file.txt | open
# 1707565076.245372 | new_file.txt | closed         0.004001.


