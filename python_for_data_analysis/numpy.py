import numpy as np

# array
a = np.array([1,2,3,4,5,6], dtype=float)
print(a) # [1. 2. 3. 4. 5. 6.]

# matrix
m = np.array([[1,2,3],[4,5,6],[7,8,9]], dtype=int)
print(m)

# [[1 2 3]
#  [4 5 6]
# [7 8 9]]

# array and matrix sizes
print(a.shape) # (6,)
print(m.shape) # (3, 3)

# shape - Вимірювання масиву: розмір масиву вздовж кожної з його осей, повертається як кортеж цілих чисел
# ndim - Кількість осей (вимірювань). Зверніть увагу: ndim == len(shape)
# size - Загальна кількість елементів у масиві, рівна добутку елементів кортежу `shape`
# dtype - Тип даних масиву (див. нижче)
# data - «Буфер» в пам'яті, що містить дійсні елементи масиву
# itemsize - Розмір у байтах кожного елемента

# Create vector or matrix with ones or zeros
v1 = np.ones(5)
print(v1) # [1. 1. 1. 1. 1]
