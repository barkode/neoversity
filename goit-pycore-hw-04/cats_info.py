from helpers import read_file
from constants import DEFAULT_CATS_INFO_PATH as DEFAULT_PATH


def get_cats_info(path: str = DEFAULT_PATH) -> list[dict]:
    """Function get cats info of given path"""
    result = []
    cats = read_file(path)

    if not cats:
        return []

    for cat in cats:
        if len(cat) < 3:
            continue

        id_num, name, age = cat[:3]
        result.append({"id": id_num, "name": name, "age": age})

    return result

if __name__ == "__main__":
    print("I'm not working in standalone mode. Please run main.py to use this function.")