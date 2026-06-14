import numpy as np

# Вектор на площині (R^2)
v_2d = np.array([3, 2])
print(f"Двовимірний вектор: {v_2d}")

# Вектор у тривимірному просторі (R^3)
v_3d = np.array([1, 4, 2])
print(f"Тривимірний вектор: {v_3d}")

# Вектор у багатовимірному просторі (R^5)
v_5d = np.array([2, -1, 3, 0, 5])
print(f"П'ятивимірний вектор: {v_5d}")

apartment = np.array([65, 2, 5, 850000])  # площа, кімнати, поверх, ціна
print("Квартира як вектор у R^4:")
print(f"Площа: {apartment[0]} м²")
print(f"Кімнат: {apartment[1]}")
print(f"Поверх: {apartment[2]}")
print(f"Ціна: {apartment[3]} грн")

student = np.array([85, 90, 78, 92, 88])  # оцінки з 5 предметів
print(f"Оцінки студента: {student}")
print(f"Середній бал: {student.mean():.2f}")
