expenses = {"hotel": 150, "breakfast": 30, "taxi": 15, "lunch": 20}

file_name = "expenses.txt"
with open(file_name, "w") as fh:
    for key, value in expenses.items():
        fh.write(f"{key}|{value}\n")

file_name = "expenses.txt"
expenses = {}

with open(file_name, "r") as fh:
    raw_expenses = fh.readlines()
    for line in raw_expenses:
        key, value = line.split("|")
        expenses[key] = int(value)

print(expenses)

import pickle

# Об'єкт для серіалізації
my_data = {"key": "value", "num": 42}

# Серіалізація об'єкта в байтовий рядок
serialized_data = pickle.dumps(my_data)
# Виведе байтовий рядок
print(f"PICkLE. Serialized Data: {serialized_data}")

# Десеріалізація об'єкта з байтового рядка
deserialized_data = pickle.loads(serialized_data)
# Виведе вихідний об'єкт Python
print(f"PICkLE. Deserialized Data: {deserialized_data}")

# Об'єкт для серіалізації
my_data = {"key": "value", "num": 100}

# Серіалізація об'єкта у файл
with open("data.pickle", "wb") as file:
    pickle.dump(my_data, file)

# Десеріалізація об'єкта з файлу
with open('data.pickle', 'rb') as file:
    deserialized_data = pickle.load(file)

# Виведе вихідний об'єкт Python
print(f"PICkLE. DESERIALIZED DATA : {deserialized_data}")


# Робота з класами користувача

class Human:
    def __init__(self, name):
        self.name = name


bob = Human("Bob")
with open("instance.pickle", "wb") as file:
    pickle.dump(bob, file)


class Human:
    def __init__(self, name):
        self.name = name


with open("instance.pickle", "rb") as file:
    loaded_instance = pickle.load(file)

print(f"PICkLE. LOADED DATA: {loaded_instance}")
print(f"PICkLE. LOADED DATA NAME: {loaded_instance.name}")

import json

some_data = {
    "key": "value",
    2: [1, 2, 3],
    "my_tuple": (5, 6),
    "my_dict": {"key": "value"},
    }

json_string = json.dumps(some_data)
print(f"JSON. JSON STRING : {json_string}")
unpacked_some_data = json.loads(json_string)
print(f"JSON. Unpacked Some Data : {unpacked_some_data}")

# Python-об'єкт (словник)
data = {"name": "Gupalo Vasyl", "age": 30, "isStudent": True}

# Серіалізація у файл
with open("data.json", "w", encoding="utf-8") as f:
    json.dump(data, f)

# Десеріалізація з файлу
with open("data.json", "r", encoding="utf-8") as f:
    data_from_file = json.load(f)
    print(f"JSON. DATA FROM FILE : {data_from_file}")

# Робота з таблицями CSV у Python
import csv

# Відкриваємо CSV-файл
print()
print("CSV. CSV FILE CONTENT:")
with open("data.csv", newline="", encoding="utf-8") as csvfile:
    # Створюємо об'єкт reader
    reader = csv.reader(csvfile, delimiter=",")
    # Проходимося по кожному рядку у файлі
    for row in reader:
        print(", ".join(row))

# Дані для запису
rows = [
    ["name", "age", "specialty"],
    ["Василь Гупало", 30, "Математика"],
    ["Марія Петренко", 22, "Фізика"],
    ["Олександр Коваленко", 20, "Інформатика"],
    ]

# Відкриваємо файл для запису
with open("data.csv", "w", newline="", encoding="utf-8") as csvfile:
    # Створюємо об'єкт writer
    writer = csv.writer(csvfile, delimiter=",")
    # Записуємо рядки даних
    writer.writerows(rows)

# Запис у CSV-файл зі словників
with open("students.csv", "w", newline="", encoding="utf-8") as csvfile:
    fieldnames = ["name", "age", "specialty"]
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()
    writer.writerow({"name": "Олег Олегов", "age": 23, "specialty": "Історія"})
    writer.writerow(
        {"name": "Анна Сергіївна", "age": 22, "specialty": "Біологія"})

# Читання з CSV-файлу в словники
with open("students.csv", newline="", encoding="utf-8") as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        print(row["name"], row["age"], row["specialty"])

import csv

FILENAME = "users.csv"

users = [
    {"name": "Микола", "age": 22, "gender": "male"},
    {"name": "Марія", "age": 22, "gender": "female"},
    {"name": "Назар", "age": 22, "gender": "male"},
    ]

with open(FILENAME, "w", encoding="utf-8", newline="") as f:
    columns = users[0].keys()
    writer = csv.DictWriter(f, delimiter=",", fieldnames=columns)
    writer.writeheader()
    for row in users:
        writer.writerow(row)

with open(FILENAME, "r", encoding="utf-8", newline="") as f:
    reader = csv.DictReader(f)

    for row in reader:
        print(row)
