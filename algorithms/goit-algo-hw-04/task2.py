import argparse
import turtle


def koch_curve(t: turtle.Turtle, length: float, level: int) -> None:
    """Малює одну криву Коха рекурсивно."""
    if level == 0:
        t.forward(length)
        return

    length /= 3.0

    koch_curve(t, length, level - 1)
    t.left(60)
    koch_curve(t, length, level - 1)
    t.right(120)
    koch_curve(t, length, level - 1)
    t.left(60)
    koch_curve(t, length, level - 1)


def koch_snowflake(t: turtle.Turtle, length: float, level: int) -> None:
    """Малює сніжинку Коха з трьох кривих Коха."""
    for _ in range(3):
        koch_curve(t, length, level)
        t.right(120)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Побудова фракталу «Сніжинка Коха»."
        )
    parser.add_argument(
        "level",
        type=int,
        nargs="?",
        default=3,
        help="Рівень рекурсії. За замовчуванням: 3.",
        )

    args = parser.parse_args()

    if args.level < 0:
        print("Рівень рекурсії не може бути від’ємним.")
        return

    screen = turtle.Screen()
    screen.title("Сніжинка Коха")
    screen.bgcolor("white")

    t = turtle.Turtle()
    t.speed(0)
    t.color("blue")
    t.pensize(1)

    length = 450
    t.penup()
    t.goto(-length / 2, length / 3)
    t.pendown()

    koch_snowflake(t, length, args.level)

    screen.mainloop()


if __name__ == "__main__":
    main()