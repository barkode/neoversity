import random

import matplotlib.pyplot as plt


def simulate_dice_rolls(num_rolls):
    counts = {sum_value: 0 for sum_value in range(2, 13)}

    # Симуляція кидків
    for _ in range(num_rolls):
        # Підрахунок кількості кидків для можливих значень сум
        dice_sum = random.randint(1, 6) + random.randint(1, 6)
        counts[dice_sum] += 1

    # Обрахування ймовірності випаду кожної суми
    probabilities = {
        sum_value: counts[sum_value] / num_rolls
        for sum_value in counts
        }

    return probabilities


def plot_probabilities(probabilities):
    sums = list(probabilities.keys())
    probs = list(probabilities.values())

    # Створення графіка
    plt.bar(sums, probs, tick_label=sums)
    plt.xlabel('Сума чисел на кубиках')
    plt.ylabel('Ймовірність')
    plt.title('Ймовірність суми чисел на двох кубиках')

    # Додавання відсотків випадання на графік
    for i, prob in enumerate(probs):
        plt.text(sums[i], prob, f"{prob * 100:.2f}%", ha='center')

    plt.show()


def print_comparison(probabilities):
    analytical_probabilities = {
        2: 1 / 36, 3: 2 / 36, 4: 3 / 36, 5: 4 / 36,
        6: 5 / 36, 7: 6 / 36, 8: 5 / 36, 9: 4 / 36,
        10: 3 / 36, 11: 2 / 36, 12: 1 / 36
        }

    print("Сума | Монте-Карло | Аналітична ймовірність | Різниця")
    for sum_value in range(2, 13):
        simulated = probabilities[sum_value]
        analytical = analytical_probabilities[sum_value]
        difference = abs(simulated - analytical)
        print(
            f"{sum_value:>4} | {simulated:>11.2%} | "
            f"{analytical:>22.2%} | {difference:.2%}"
            )


if __name__ == "__main__":
    for accuracy in [100, 1000, 10000, 10000]:
        # Симуляція кидків і обчислення ймовірностей
        probabilities = simulate_dice_rolls(accuracy)

        # Порівняння з аналітичними розрахунками
        print(f"Кількість кидків: {accuracy}")
        print_comparison(probabilities)

        # Відображення ймовірностей на графіку
        plot_probabilities(probabilities)
