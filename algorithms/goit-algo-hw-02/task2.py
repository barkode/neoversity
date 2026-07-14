from collections import deque


def is_palindrome(text: str) -> bool:
    normalized_text = "".join(text.lower().split())
    characters = deque(normalized_text)
    
    while len(characters) > 1:
        if characters.pop() != characters.popleft():
            return False

    return True

def main():
    examples = [
        "А роза упала на лапу Азора",
        "level",
        "Кіт утік",
        "12321",
        "12345",
        "АББА",
        ]

    for text in examples:
        result = "IT'S A PALINDROME" if is_palindrome(text) else "IT'S NOT A PALINDROME"
        print(f"{text} - {result}")

if __name__ == "__main__":
    main()