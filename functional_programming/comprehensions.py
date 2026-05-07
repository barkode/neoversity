sq = []
for i in range(1, 6):
    sq.append(i ** 2)

print(sq)  # [1, 4, 9, 16, 25]

# List Comprehensions
print("List Comprehensions")
# [new_item for item in iterable if condition]

sq = [x ** 2 for x in range(1, 6)]
print(sq)  # [1, 4, 9, 16, 25]

# if condition
even_squares = [x ** 2 for x in range(1, 10) if x % 2 == 0]
print(f"ONLY EVEN SQUARES : {even_squares}")  # [4, 16, 36, 64]

# without comprehension
print("without comprehension")
even_squares = []
for x in range(1, 10):
    if x % 2 == 0:
        even_squares.append(x ** 2)

print(f"ONLY EVEN SQUARES : {even_squares}")  # [4, 16, 36, 64]

# Set Comprehensions
print("Set Comprehensions")
# {new_item for item in iterable if condition}

numbers = [1, 4, 1, 3, 2, 5, 2, 6]
sq = {i ** 2 for i in numbers}

print(sq)  # {1, 4, 9, 16, 25, 36}

# if condition
odd_squares = {x ** 2 for x in range(1, 10) if x % 2 != 0}
print(f"Only ODD SQUARES : {odd_squares}")  # [1, 9, 81, 49, 25}

# Dictionary Comprehensions
print("Dictionary Comprehensions")
# {key: value for item in iterable if condition}

sq = {x: x ** 2 for x in range(1, 10)}
print(sq)  # {1: 1, 2: 4, 3: 9, 4: 16, 5: 25, 6: 36, 7: 49, 8: 64, 9: 81}

sq_dict = {x: x ** 2 for x in range(1, 10) if x > 5}
print(f"All NUMBERS > 5 : {sq_dict}")
