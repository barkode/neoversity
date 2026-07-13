# lambda functions
# lambda arguments: expression

# BAD practice
add = lambda x, y: x + y
print(add(5, 3))  # Виведе 8

# GOOD practice
print((lambda x, y: x + y)(5, 3))  # 8

# reverse sorted
nums = [1, 2, 3, 4, 5]
nums_sorted = sorted(nums, key=lambda x: -x)
print(nums_sorted)  # [5, 4, 3, 2, 1]

# map function
print("map generator")
# map(function, iterable, ...)

# Generator
numbers = [1, 2, 3, 4, 5]
for i in map(lambda x: x ** 2, numbers):
    print(i)  # 1 4 9 16 25

# List

numbers = [1, 2, 3, 4, 5]
squared_nums = list(map(lambda x: x ** 2, numbers))
print(squared_nums)  # [1, 4, 9, 16, 25]

# for two lists
nums1 = [1, 2, 3]
nums2 = [4, 5, 6]
sum_nums = map(lambda x, y: x + y, nums1, nums2)
print(list(sum_nums))  # [5, 7, 9]

# filter function
# filter(function, iterable)
even_nums = filter(lambda x: x % 2 == 0, range(1, 11))
print(list(even_nums))


# use common function
def is_positive(x) -> bool:
    return x > 0


nums = [-2, -1, 0, 1, 2]
positive_nums = filter(is_positive, nums)
print(list(positive_nums))  # [1, 2]

some_str = 'abcdefgHiGKLmnopqrSTUvWxyZ'
new_str = ''.join(list(filter(lambda x: x.islower(), some_str)))
print(new_str)  # abcdefgmnopqrxy

# list comprehensions instead filter()
nums = [1, 2, 3, 4, 5, 6]
even_nums = [x for x in nums if x % 2 == 0]
print(even_nums)  # [2, 4, 6]

some_str = 'Видавництво А-БА-БА-ГА-ЛА-МА-ГА'

new_str = ''.join([x for x in some_str if x.islower()])
print(new_str)  # идавництво

# any()
nums = [0, False, 5, 0]
result = any(nums)
print(result)  # True

nums = [1, 3, 5, 7, 9]
result = any(x % 2 == 0 for x in nums)
print(result)  # False

# all()
nums = [1, 2, 3, 4, 5]
result = all(nums)
print(result)  # True

nums = [1, 2, 3, 4]
is_all_even = all(x % 2 == 0 for x in nums)
print(is_all_even)  # False

words = ["Hello", "World", "Python"]
is_all_title_case = all(word.istitle() for word in words)
print(is_all_title_case)  # True
