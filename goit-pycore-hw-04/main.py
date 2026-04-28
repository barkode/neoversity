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
    result = []
    cats = read_file(path)
    print(cats)

    if not cats:
        return []

    for cat in cats:
        id_num, name, age = cat
        result.append({"id": id_num, "name": name, "age": age})

    return result


def read_file(path) -> list[str]:
    try:
        lines = []
        with open(path, encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    line = tuple(line.split(','))
                    lines.append(line)
                except (ValueError, IndexError):
                    print(f'Error in line {line}')
                    continue
        return lines

    except FileNotFoundError:
        print(f'File {path} not found')
        return []

# total, average = total_salary("salary.txt")
# print(
#     f"Загальна сума заробітної плати: {total}, Середня заробітна плата: {average}")
#
cats_info = get_cats_info("cats.txt")
print(cats_info)