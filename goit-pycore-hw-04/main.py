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
    pass


b = total_salary('salary.txt')
print(b)
