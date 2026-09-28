"""
main.py — CRUD-операції з MongoDB для колекції котів.

Структура документа:
    {
        "_id": ObjectId(...),
        "name": "barsik",
        "age": 3,
        "features": ["ходить в капці", "дає себе гладити", "рудий"]
    }

Залежності:
    pip install pymongo

Налаштування:
    Змініть MONGO_URI нижче відповідно до вашого середовища.
    За замовчуванням підключається до локального MongoDB на порту 27017.
"""

from pymongo import MongoClient
from pymongo.errors import PyMongoError

# ── Параметри підключення до MongoDB ─────────────────────────────────────────
MONGO_URI   = "mongodb://localhost:27017/"   # або ваш Atlas URI
DB_NAME     = "cats_db"
COLLECTION  = "cats"
# ─────────────────────────────────────────────────────────────────────────────


def get_collection():
    """
    Встановлює з'єднання з MongoDB та повертає колекцію котів.

    Returns:
        pymongo.collection.Collection — об'єкт колекції.

    Raises:
        PyMongoError: якщо не вдалося підключитися.
    """
    client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
    # Перевірка доступності сервера
    client.admin.command("ping")
    db = client[DB_NAME]
    return db[COLLECTION]


# ════════════════════════════════════════════════════════════════════════════
# CREATE
# ════════════════════════════════════════════════════════════════════════════

def create_cat(name: str, age: int, features: list[str]) -> None:
    """
    Додає нового кота до колекції.

    Args:
        name:     ім'я кота.
        age:      вік кота (роки).
        features: список характеристик кота.
    """
    try:
        col = get_collection()
        doc = {"name": name, "age": age, "features": features}
        result = col.insert_one(doc)
        print(f"✅ Кота '{name}' додано. _id = {result.inserted_id}")
    except PyMongoError as e:
        print(f"❌ Помилка при додаванні кота: {e}")


# ════════════════════════════════════════════════════════════════════════════
# READ
# ════════════════════════════════════════════════════════════════════════════

def read_all_cats() -> None:
    """Виводить усі записи з колекції котів."""
    try:
        col = get_collection()
        cats = list(col.find())
        if not cats:
            print("📭 Колекція порожня.")
            return
        print(f"\n{'─' * 50}")
        print(f"  Усі коти ({len(cats)} записів):")
        print(f"{'─' * 50}")
        for cat in cats:
            _print_cat(cat)
        print(f"{'─' * 50}\n")
    except PyMongoError as e:
        print(f"❌ Помилка при читанні колекції: {e}")


def read_cat_by_name(name: str) -> None:
    """
    Виводить інформацію про кота за іменем.

    Args:
        name: ім'я кота для пошуку.
    """
    try:
        col = get_collection()
        cat = col.find_one({"name": name})
        if cat:
            print(f"\nЗнайдено кота '{name}':")
            _print_cat(cat)
        else:
            print(f"⚠️  Кота з іменем '{name}' не знайдено.")
    except PyMongoError as e:
        print(f"❌ Помилка при пошуку кота: {e}")


# ════════════════════════════════════════════════════════════════════════════
# UPDATE
# ════════════════════════════════════════════════════════════════════════════

def update_cat_age(name: str, new_age: int) -> None:
    """
    Оновлює вік кота за іменем.

    Args:
        name:    ім'я кота.
        new_age: новий вік кота.
    """
    try:
        col = get_collection()
        result = col.update_one(
            {"name": name},
            {"$set": {"age": new_age}}
            )
        if result.matched_count:
            print(f"✅ Вік кота '{name}' оновлено до {new_age} років.")
        else:
            print(f"⚠️  Кота з іменем '{name}' не знайдено.")
    except PyMongoError as e:
        print(f"❌ Помилка при оновленні віку: {e}")


def add_feature_to_cat(name: str, feature: str) -> None:
    """
    Додає нову характеристику до списку features кота.

    Args:
        name:    ім'я кота.
        feature: нова характеристика для додавання.
    """
    try:
        col = get_collection()
        result = col.update_one(
            {"name": name},
            {"$addToSet": {"features": feature}}   # $addToSet — не дублює
            )
        if result.matched_count:
            print(f"✅ Характеристику '{feature}' додано до кота '{name}'.")
        else:
            print(f"⚠️  Кота з іменем '{name}' не знайдено.")
    except PyMongoError as e:
        print(f"❌ Помилка при додаванні характеристики: {e}")


# ════════════════════════════════════════════════════════════════════════════
# DELETE
# ════════════════════════════════════════════════════════════════════════════

def delete_cat_by_name(name: str) -> None:
    """
    Видаляє запис кота з колекції за іменем.

    Args:
        name: ім'я кота для видалення.
    """
    try:
        col = get_collection()
        result = col.delete_one({"name": name})
        if result.deleted_count:
            print(f"✅ Кота '{name}' видалено з колекції.")
        else:
            print(f"⚠️  Кота з іменем '{name}' не знайдено.")
    except PyMongoError as e:
        print(f"❌ Помилка при видаленні кота: {e}")


def delete_all_cats() -> None:
    """Видаляє всі записи з колекції котів."""
    try:
        col = get_collection()
        result = col.delete_many({})
        print(f"✅ Видалено {result.deleted_count} записів із колекції.")
    except PyMongoError as e:
        print(f"❌ Помилка при очищенні колекції: {e}")


# ════════════════════════════════════════════════════════════════════════════
# Допоміжні функції
# ════════════════════════════════════════════════════════════════════════════

def _print_cat(cat: dict) -> None:
    """Форматований вивід одного запису кота."""
    print(f"  _id      : {cat['_id']}")
    print(f"  Ім'я     : {cat.get('name', '—')}")
    print(f"  Вік      : {cat.get('age', '—')} р.")
    print(f"  Риси     : {', '.join(cat.get('features', []))}")
    print()


# ════════════════════════════════════════════════════════════════════════════
# Демонстраційний запуск
# ════════════════════════════════════════════════════════════════════════════

def main():
    """Демонстрація всіх CRUD-операцій."""
    print("=" * 55)
    print("  MongoDB CRUD — колекція котів")
    print("=" * 55)

    # CREATE — додаємо початкові записи
    print("\n[CREATE] Додавання котів:")
    create_cat("barsik", 3, ["ходить в капці", "дає себе гладити", "рудий"])
    create_cat("murzik", 5, ["любить рибу", "спить цілий день"])
    create_cat("pushok", 1, ["грайливий", "кусається", "білий"])

    # READ — читаємо всі записи
    print("\n[READ] Всі коти:")
    read_all_cats()

    # READ — пошук за іменем
    print("[READ] Пошук кота 'murzik':")
    read_cat_by_name("murzik")

    # UPDATE — оновлення віку
    print("\n[UPDATE] Оновлення віку 'barsik' → 4:")
    update_cat_age("barsik", 4)
    read_cat_by_name("barsik")

    # UPDATE — додавання характеристики
    print("[UPDATE] Додавання риси 'любить грітися' до 'pushok':")
    add_feature_to_cat("pushok", "любить грітися")
    read_cat_by_name("pushok")

    # DELETE — видалення одного кота
    print("[DELETE] Видалення 'murzik':")
    delete_cat_by_name("murzik")
    read_all_cats()

    # DELETE — видалення всіх котів
    print("[DELETE] Видалення всіх котів:")
    delete_all_cats()
    read_all_cats()


if __name__ == "__main__":
    main()
