import random
import pathlib

current_dir = pathlib.Path(__file__).parent

def get_random_joke():
    try:
        with open(current_dir / 'jokes.txt', 'r', encoding='utf-8') as f:
            jokes = f.readlines()
            return random.choice(jokes).strip()
    except FileNotFoundError:
        return "Sorry, I couldn't find the jokes file."
    except Exception as e:
        return f"An error occurred: {e}"

