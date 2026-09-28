"""
create_tables.py — Скрипт створення таблиць для системи управління завданнями.

Створює таблиці users, status, tasks у PostgreSQL та заповнює
таблицю status початковими значеннями статусів.

Залежності:
    pip install psycopg2-binary

Налаштування:
    Змініть константи DB_* нижче відповідно до вашого середовища.
"""

import psycopg2
from psycopg2 import sql
from psycopg2.errors import DuplicateTable

# ── Параметри підключення до PostgreSQL ──────────────────────────────────────
DB_HOST     = "localhost"
DB_PORT     = 5432
DB_NAME     = "task_manager"   # назва бази даних
DB_USER     = "postgres"       # ваш PostgreSQL користувач
DB_PASSWORD = "password"       # ваш PostgreSQL пароль
# ─────────────────────────────────────────────────────────────────────────────

# SQL-команди для створення таблиць
CREATE_USERS_TABLE = """
CREATE TABLE IF NOT EXISTS users (
    id       SERIAL PRIMARY KEY,
    fullname VARCHAR(100) NOT NULL,
    email    VARCHAR(100) NOT NULL UNIQUE
);
"""

CREATE_STATUS_TABLE = """
CREATE TABLE IF NOT EXISTS status (
    id   SERIAL PRIMARY KEY,
    name VARCHAR(50) NOT NULL UNIQUE
);
"""

CREATE_TASKS_TABLE = """
CREATE TABLE IF NOT EXISTS tasks (
    id          SERIAL PRIMARY KEY,
    title       VARCHAR(100) NOT NULL,
    description TEXT,
    status_id   INTEGER NOT NULL REFERENCES status(id),
    user_id     INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE
);
"""

# Початкові значення статусів
INITIAL_STATUSES = [("new",), ("in progress",), ("completed",)]


def get_connection():
    """
    Встановлює та повертає з'єднання з базою даних PostgreSQL.

    Returns:
        psycopg2 connection object.

    Raises:
        psycopg2.OperationalError: якщо не вдалося підключитися.
    """
    return psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
    )


def create_tables(cursor) -> None:
    """
    Виконує SQL-команди для створення таблиць users, status, tasks.

    Порядок створення важливий: спочатку незалежні таблиці (users, status),
    потім залежна (tasks), яка містить зовнішні ключі.

    Args:
        cursor: курсор бази даних.
    """
    print("  Створення таблиці 'users'...")
    cursor.execute(CREATE_USERS_TABLE)

    print("  Створення таблиці 'status'...")
    cursor.execute(CREATE_STATUS_TABLE)

    print("  Створення таблиці 'tasks' (з ON DELETE CASCADE на user_id)...")
    cursor.execute(CREATE_TASKS_TABLE)


def seed_statuses(cursor) -> None:
    """
    Додає початкові статуси до таблиці status (якщо вони ще не існують).

    Використовує INSERT ... ON CONFLICT DO NOTHING, щоб уникнути
    дублювання при повторному запуску скрипту.

    Args:
        cursor: курсор бази даних.
    """
    print("  Заповнення таблиці 'status' початковими значеннями...")
    cursor.executemany(
        "INSERT INTO status (name) VALUES (%s) ON CONFLICT (name) DO NOTHING;",
        INITIAL_STATUSES,
    )


def main():
    """Головна функція: підключається до БД та створює структуру таблиць."""
    print("=== Створення структури бази даних task_manager ===\n")
    conn = None
    cursor = None
    try:
        print("Підключення до PostgreSQL...")
        conn = get_connection()
        cursor = conn.cursor()

        create_tables(cursor)
        seed_statuses(cursor)

        conn.commit()
        print("\n✅ Таблиці успішно створено та ініціалізовано.")

        # Виводимо підтвердження існуючих таблиць
        cursor.execute("""
            SELECT table_name
            FROM information_schema.tables
            WHERE table_schema = 'public'
            ORDER BY table_name;
        """)
        tables = [row[0] for row in cursor.fetchall()]
        print(f"   Таблиці в БД: {', '.join(tables)}")

        # Виводимо статуси, що були додані
        cursor.execute("SELECT id, name FROM status ORDER BY id;")
        statuses = cursor.fetchall()
        print(f"   Статуси: {statuses}")

    except psycopg2.OperationalError as e:
        print(f"\n❌ Помилка підключення до БД: {e}")
        print("   Перевірте параметри DB_* на початку файлу.")
    except psycopg2.Error as e:
        if conn:
            conn.rollback()
        print(f"\n❌ Помилка бази даних: {e}")
    except Exception as e:
        if conn:
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
