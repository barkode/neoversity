import numpy as np
# Вектори в площині xy (z = 0)
a = np.array([1, 0, 0])
b = np.array([0, 1, 0])
c = np.array([2, 3, 0])  # c = 2*a + 3*b

print("Вектори в площині xy:")
print(f"  a = {a}")
print(f"  b = {b}")
print(f"  c = {c}")
print(f"Усі мають z = 0, тому лежать в одній площині")
print(f"Вираження c через a та b:")
print(f"  c = 2×a + 3×b = 2×{a} + 3×{b} = {2*a + 3*b}")
print(f"  Перевірка: {np.allclose(c, 2*a + 3*b)}")

# Linear Independency
