from helpers import read_file

DEFAULT_PATH = "cats_info.txt"

def get_cats_info(path: str = DEFAULT_PATH) -> list[dict]:
    """Function get cats info of given path"""
    result = []
    cats = read_file(path)

    if not cats:
        return []

    for cat in cats:
        id_num, name, age, *rest = cat
        result.append({"id": id_num, "name": name, "age": age})

    return result