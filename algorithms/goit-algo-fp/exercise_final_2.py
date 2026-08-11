import matplotlib.pyplot as plt
import numpy as np


def draw_branch(x, y, angle, length, depth):
    """
    Рекурсивна функція для малювання гілки дерева Піфагора.

    Параметри:
        x, y    — координати початку гілки
        angle   — кут нахилу гілки (в радіанах)
        length  — довжина поточної гілки
        depth   — поточний рівень рекурсії (зменшується до 0)
    """
    if depth == 0:
        return

    # Координати кінця поточної гілки
    x_end = x + length * np.cos(angle)
    y_end = y + length * np.sin(angle)

    # Колір залежить від глибини: від коричневого (стовбур) до зеленого (листя)
    t = depth / max_depth
    color = (0.4 - 0.4 * t, 0.2 + 0.6 * t,
             0.0)  # RGB від зеленого до коричневого

    # Товщина лінії зменшується разом із глибиною
    linewidth = 1 + depth * 0.5

    plt.plot([x, x_end], [y, y_end], color=color, linewidth=linewidth)

    # Ліва гілка: повертаємо на 45° вліво, зменшуємо довжину
    draw_branch(x_end, y_end, angle + np.radians(45), length * 0.7, depth - 1)

    # Права гілка: повертаємо на 45° вправо, зменшуємо довжину
    draw_branch(x_end, y_end, angle - np.radians(45), length * 0.7, depth - 1)


# ── Введення рівня рекурсії користувачем ────────────────────────────────────
while True:
    try:
        max_depth = int(
            input("Введіть рівень рекурсії (ціле число від 1 до 15): "))
        if 1 <= max_depth <= 15:
            break
        else:
            print("Будь ласка, введіть число від 1 до 15.")
    except ValueError:
        print("Некоректне введення. Введіть ціле число.")

# ── Налаштування вікна для малювання ────────────────────────────────────────
plt.figure(figsize=(10, 10))
plt.title(f"Дерево Піфагора  (рівень рекурсії = {max_depth})", fontsize=14)
plt.axis('off')
plt.gca().set_aspect('equal')

# Початкова гілка: знизу по центру, напрямок — вертикально вгору (90°)
start_length = 100
draw_branch(0, 0, np.radians(90), start_length, max_depth)

plt.tight_layout()

# Зберігаємо результат у файл
output_file = f"pythagorean_tree_depth_{max_depth}.png"
plt.savefig(output_file, dpi=150, bbox_inches='tight')
print(f"Фрактал збережено у файл: {output_file}")

plt.show()
