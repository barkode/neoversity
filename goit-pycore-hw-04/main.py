import sys
import calculate_total_salary
import cats_info

EXIT_PHRASES = ['quit', 'exit', 'q', 'logoff']


def main():
    while True:
        print()
        user_input = input("Введіть команду (або 'quit' для виходу): ").strip().lower()
        if user_input in EXIT_PHRASES:
            print("Вихід з програми. До побачення!")
            break
        else:
            print(f"Ви ввели: {user_input}")
    sys.exit(0)


if __name__ == "__main__":
    main()
    sys.exit(0)
