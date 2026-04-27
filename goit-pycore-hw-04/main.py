def total_salary(path: str) -> tuple[int, int]:
    """Function calculate total salary of given path"""
    try:
        salaries = []
        with open(path, encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    _, salary = line.split(',')
                    salaries.append(float(salary))
                except (ValueError, IndexError):
                    print(f'Error in line {line}')
                    continue

        if not salaries:
            return 0, 0

        total = sum(salaries)
        average = total / len(salaries)
        return int(total), int(average)
    except FileNotFoundError:
        print(f'File {path} not found')
        return 0, 0


def get_cats_info(path) -> list[dict]:
    """Function get cats info of given path"""
    try:
        cats = []
        with open(path, encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    id_num, name, age = line.split(',')
                    cats.append({"id": id_num, "name": name, "age": age})
                except (ValueError, IndexError):
                    print(f'Error in line {line}')
                    continue

        if not cats:
            return []

        return cats

    except FileNotFoundError:
        print(f'File {path} not found')
        return []


def read_file(path: str) -> list[str]:
    try:
        lines = []
        with open(path, encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                line = tuple(line.split(','))
                lines.append(line)
    except FileNotFoundError:
        print(f'File {path} not found')
        return []
    return lines


# total, average = total_salary("salary.txt")
# print(
#     f"Загальна сума заробітної плати: {total}, Середня заробітна плата: {average}")
#
# cats_info = get_cats_info("cats.txt")
# print(cats_info)

b = read_file("cats.txt")
print(b)

c = read_file("salary.txt")
print(c)