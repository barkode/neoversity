import numpy as np

# Визначаємо два вектори у R^3
a = np.array([1, 2, 3])
b = np.array([4, 5, 6])

# Виконуємо додавання
c = a + b

print("Вектор a:", a)
print("Вектор b:", b)
print("Сума a + b:", c)

# Базовий вектор
v = np.array([2, 3])

# Множення на різні скаляри
scalars = [0.5, 1, 2, -1]
results = {}

print("Множення вектора v = [2, 3] на різні скаляри:\\n")
for alpha in scalars:
    result = alpha * v
    results[alpha] = result
    print(f"  {alpha} × v = {result}")

# Вектор ознак (наприклад, вік, зарплата, стаж)
features = np.array([35, 50000, 7])
print("Оригінальні ознаки:", features)
print("  Вік: 35 років")
print("  Зарплата: 50000 грн")
print("  Стаж: 7 років")

# Масштабування кожної ознаки до діапазону [0, 1]
# Для простоти припустимо максимальні значення
max_values = np.array([100, 200000, 40])
normalized = features / max_values

print("Нормалізовані ознаки:", normalized)
print(f"  Вік: {normalized[0]:.2f} (35/100)")
print(f"  Зарплата: {normalized[1]:.2f} (50000/200000)")
print(f"  Стаж: {normalized[2]:.2f} (7/40)")

# Linear combination of vectors
# Одиничні вектори вздовж осей координат
e1 = np.array([1, 0])  # одиничний вектор по осі x
e2 = np.array([0, 1])  # одиничний вектор по осі y

# Довільний вектор
target = np.array([3, 2])

# Представлення через одиничні вектори
result = 3*e1 + 2*e2

print("Одиничні вектори вздовж осей:")
print(f"  e₁ = {e1} (вздовж осі x)")
print(f"  e₂ = {e2} (вздовж осі y)")
print(f"Цільовий вектор: {target}")
print(f"Лінійна комбінація:")
print(f"  3×e₁ + 2×e₂ = 3×{e1} + 2×{e2} = {result}")
print(f"Перевірка: {np.array_equal(result, target)}")

# Основні кольори у RGB-просторі (значення від 0 до 255)
red = np.array([255, 0, 0])
green = np.array([0, 255, 0])
blue = np.array([0, 0, 255])

print("Основні кольори:")
print(f"  Червоний: {red}")
print(f"  Зелений:  {green}")
print(f"  Синій:    {blue}")

# Отримуємо нові кольори через лінійні комбінації
olive = 0.5*red + 0.5*green + 0*blue
purple = 0.5*red + 0*green + 0.5*blue
cyan = 0*red + 0.5*green + 0.5*blue
white = 0.33*red + 0.33*green + 0.33*blue

print("\\nНові кольори (лінійні комбінації):")
print(f"  Оливковий:     {olive.astype(int)} = 0.5×red + 0.5×green")
print(f"  Пурпуровий: {purple.astype(int)} = 0.5×red + 0.5×blue")
print(f"  Темно-бірюзовий:  {cyan.astype(int)} = 0.5×green + 0.5×blue")
print(f"  Темно-сірий:      {white.astype(int)} = 0.33×red + 0.33×green + 0.33×blue")
