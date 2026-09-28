"""
seed.py — Скрипт для заповнення бази даних системи управління завданнями
випадковими даними за допомогою бібліотеки Faker.

Залежності:
    pip install psycopg2-binary faker

Налаштування підключення до PostgreSQL:
    Змініть константи DB_* нижче відповідно до вашого середовища.
"""

import random
import psycopg2
from faker import Faker

# ── Параметри підключення до PostgreSQL ──────────────────────────────────────
DB_HOST = "localhost"
DB_PORT = 5432
DB_NAME = "task_manager"   # назва бази даних
DB_USER = "postgres"       # ваш PostgreSQL користувач
DB_PASSWORD = "password"   # ваш PostgreSQL пароль
# ─────────────────────────────────────────────────────────────────────────────

# Кількість записів, які буде додано
NUM_USERS = 10
NUM_TASKS = 20

fake = Faker("uk_UA")   # українська локаль для реалістичних імен


def get_connection():
    """Встановлює та повертає з'єднання з базою даних PostgreSQL."""
    return psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
    )


def seed_users(cursor, count: int) -> list[int]:
    """
    Додає випадкових користувачів до таблиці users.

    Args:
        cursor: курсор бази даних.
        count:  кількість користувачів для додавання.

    Returns:
        Список id доданих користувачів.
    """
    user_ids = []
    emails_used = set()

    for _ in range(count):
        fullname = fake.name()
        # Генерація унікального email
        while True:
            email = fake.unique.email()
            if email not in emails_used:
                emails_used.add(email)
                break

        cursor.execute(
            "INSERT INTO users (fullname, email) VALUES (%s, %s) RETURNING id;",
            (fullname, email),
        )
        user_id = cursor.fetchone()[0]
        user_ids.append(user_id)
        print(f"  [users] Додано: {fullname} <{email}>  (id={user_id})")

    return user_ids


def seed_tasks(cursor, user_ids: list[int], count: int) -> None:
    """
    Додає випадкові завдання до таблиці tasks.

    Args:
        cursor:   курсор бази даних.
        user_ids: список id існуючих користувачів.
        count:    кількість завдань для додавання.
    """
    # Отримуємо id всіх статусів
    cursor.execute("SELECT id FROM status;")
    status_ids = [row[0] for row in cursor.fetchall()]

    for _ in range(count):
        title = fake.bs().capitalize()[:100]   # коротка бізнес-фраза як назва
        # ~30% завдань не матимуть опису (для перевірки запиту 12)
        description = fake.text(max_nb_chars=200) if random.random() > 0.3 else None
        status_id = random.choice(status_ids)
        user_id = random.choice(user_ids)

        cursor.execute(
            """
            INSERT INTO tasks (title, description, status_id, user_id)
            VALUES (%s, %s, %s, %s) RETURNING id;
            """,
            (title, description, status_id, user_id),
        )
        task_id = cursor.fetchone()[0]
        print(
            f"  [tasks] Додано: \"{title}\"  "
            f"status_id={status_id}, user_id={user_id}  (id={task_id})"
        )


def main():
    """Головна функція: підключається до БД та виконує заповнення даними."""
    print("=== Підключення до PostgreSQL ===")
    try:
        conn = get_connection()
        conn.autocommit = False
        cursor = conn.cursor()

        print(f"\n--- Додавання {NUM_USERS} користувачів ---")
        user_ids = seed_users(cursor, NUM_USERS)

        print(f"\n--- Додавання {NUM_TASKS} завдань ---")
        seed_tasks(cursor, user_ids, NUM_TASKS)

        conn.commit()
        print("\n✅ Дані успішно збережено до бази даних.")

    except psycopg2.Error as e:
        conn.rollback()
        print(f"\n❌ Помилка бази даних: {e}")
    except Exception as e:
        conn.rollback()
        print(f"\n❌ Непередбачена помилка: {e}")
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
            print("З'єднання закрито.")


if __name__ == "__main__":
    main()
