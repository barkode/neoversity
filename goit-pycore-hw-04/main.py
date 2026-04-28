def total_salary(path: str) -> tuple[int, int]:
    """Function calculate total salary of given path"""
    result = []
    salaries = read_file(path)

    if salaries is None or not salaries:
        return 0, 0

    for salary in salaries:
        _, person_salary = salary
        result.append(float(person_salary))

    total = sum(result)
    average = total / len(salaries)
    return int(total), int(average)


def get_cats_info(path) -> list[dict]:
    """Function get cats info of given path"""
    result = []
    cats = read_file(path)

    if cats is None or not cats:
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
        return None


total, average = total_salary("salary.txt")
print(
    f"Загальна сума заробітної плати: {total}, Середня заробітна плата: {average}")

cats_info = get_cats_info("cats.txt")
print(cats_info)
