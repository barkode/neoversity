def my_generator():
    yield "Hello"
    yield "My Generator"
    yield "Goodbye"


gen = my_generator()

print(next(gen))
print(next(gen))
print(next(gen))


def count_down(start):
    while start > 0:
        yield start
        start -= 1


for number in count_down(5):
    print(number)

# File iteration
def read_lines(file_path):
    with open(file_path, "r", encoding='utf-8') as file:
        for line in file:
            yield line.strip()

# Using a generator to read lines from a file
for line in read_lines("my_file.txt"):
    print(line)