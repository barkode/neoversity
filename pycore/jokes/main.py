from joke import get_random_joke

def main():
    name = input("What's your name? ")
    print(f'Hello {name}!')

    while True:
        user_response = input(f"Do you want a new joke? (y/n):  ").lower()
        if user_response == "y":
            print(get_random_joke())
        elif user_response == "n":
            print(f'Goodbye, {name}!')
            break

if __name__ == '__main__':
    main()
