from helpers import read_file

DEFAULT_PATH = "salaries.txt"

def calculate_total_salary(path: str = DEFAULT_PATH) -> tuple[int, int]:
    """Function calculate total salary of given path"""
    result = []
    salaries = read_file(path)

    if not salaries:
        return 0, 0

    for salary in salaries:
        _, person_salary, *rest = salary
        result.append(float(person_salary))

    total = sum(result)
    average = total / len(result)
    return int(total), int(average)