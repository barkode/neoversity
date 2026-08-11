import matplotlib.pyplot as plt
import numpy as np
import scipy.integrate as spi


def f(x):
    """Функція для інтегрування."""
    return x ** 2


def monte_carlo_integral(func, a, b, samples=100_000):
    """
    Обчислює визначений інтеграл методом Монте-Карло
    методом підрахунку точок у прямокутнику.
    """
    np.random.seed(42)

    x_random = np.random.uniform(a, b, samples)

    y_min = 0
    y_max = max(func(a), func(b))
    y_random = np.random.uniform(y_min, y_max, samples)

    points_under_curve = y_random <= func(x_random)
    rectangle_area = (b - a) * (y_max - y_min)

    integral_estimate = rectangle_area * np.mean(points_under_curve)

    return integral_estimate, x_random, y_random, points_under_curve


if __name__ == "__main__":
    a = 0
    b = 2
    samples = 100_000

    monte_carlo_result, x_random, y_random, under_curve = monte_carlo_integral(
        f, a, b, samples
        )

    quad_result, quad_error = spi.quad(f, a, b)

    analytical_result = 8 / 3
    absolute_error = abs(monte_carlo_result - quad_result)

    print(f"Метод Монте-Карло: {monte_carlo_result:.6f}")
    print(f"quad: {quad_result:.6f}")
    print(f"Оцінка похибки quad: {quad_error:.2e}")
    print(f"Аналітичний результат: {analytical_result:.6f}")
    print(f"Абсолютна похибка Монте-Карло: {absolute_error:.6f}")

    x = np.linspace(-0.5, 2.5, 400)
    y = f(x)

    fig, ax = plt.subplots(figsize=(10, 6))

    ax.plot(x, y, "r", linewidth=2, label="f(x) = x²")

    ix = np.linspace(a, b, 400)
    iy = f(ix)
    ax.fill_between(ix, iy, color="gray", alpha=0.3,
                    label="Площа інтегрування")

    ax.scatter(
        x_random[under_curve],
        y_random[under_curve],
        color="green",
        s=1,
        alpha=0.3,
        label="Точки під графіком",
        )

    ax.scatter(
        x_random[~under_curve],
        y_random[~under_curve],
        color="blue",
        s=1,
        alpha=0.2,
        label="Точки поза графіком",
        )

    ax.set_xlim([x[0], x[-1]])
    ax.set_ylim([0, max(y) + 0.1])
    ax.set_xlabel("x")
    ax.set_ylabel("f(x)")
    ax.axvline(x=a, color="gray", linestyle="--")
    ax.axvline(x=b, color="gray", linestyle="--")
    ax.set_title("Інтегрування f(x) = x² від 0 до 2 методом Монте-Карло")

    plt.grid()
    plt.legend()
    plt.show()
