"""
Лабораторна робота № 8. Підключення до бази даних та виконання основних операцій.
Варіант 11: База даних «Ферма» (farm.db) з таблицею «Тварини» (animals).
Студент: Фесюк Максим Ігорович (КН-25-2)
"""
import os
import sqlite3
from typing import List, Tuple

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DEFAULT_DB_PATH = os.path.join(BASE_DIR, "farm.db")

AnimalRow = Tuple[int, str, str, int, float, str]


def get_connection(db_path: str = DEFAULT_DB_PATH) -> sqlite3.Connection:
    """Встановлює з'єднання з базою даних SQLite «Ферма»."""
    return sqlite3.connect(db_path)


def create_animals_table(conn: sqlite3.Connection) -> None:
    """Створює таблицю animals (Тварини) з різними типами даних та первинним ключем."""
    create_query = """
    CREATE TABLE IF NOT EXISTS animals (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        species VARCHAR(100) NOT NULL,
        name VARCHAR(100) NOT NULL,
        age INTEGER NOT NULL,
        weight REAL NOT NULL,
        arrival_date DATE NOT NULL
    );
    """
    with conn:
        conn.execute(create_query)


def reset_animals_table(conn: sqlite3.Connection) -> None:
    """Очищує таблицю перед демонстраційним заповненням, щоб уникнути дублювання."""
    with conn:
        conn.execute("DELETE FROM animals;")
        conn.execute("DELETE FROM sqlite_sequence WHERE name = 'animals';")


def insert_animals(
    conn: sqlite3.Connection, animals_data: List[Tuple[str, str, int, float, str]]
) -> int:
    """Вставляє список записів про тварин у таблицю animals."""
    insert_query = """
    INSERT INTO animals (species, name, age, weight, arrival_date)
    VALUES (?, ?, ?, ?, ?);
    """
    with conn:
        cur = conn.executemany(insert_query, animals_data)
        return cur.rowcount


def update_animal_weight_and_age(
    conn: sqlite3.Connection, name: str, new_weight: float, new_age: int
) -> int:
    """Оновлює вагу та вік тварини за її кличкою."""
    update_query = """
    UPDATE animals
    SET weight = ?, age = ?
    WHERE name = ?;
    """
    with conn:
        cur = conn.execute(update_query, (new_weight, new_age, name))
        return cur.rowcount


def delete_animal_by_name(conn: sqlite3.Connection, name: str) -> int:
    """Видаляє запис про тварину за її кличкою."""
    delete_query = "DELETE FROM animals WHERE name = ?;"
    with conn:
        cur = conn.execute(delete_query, (name,))
        return cur.rowcount


def select_all_animals(conn: sqlite3.Connection) -> List[AnimalRow]:
    """Повертає всі записи з таблиці animals, відсортовані за ID."""
    cur = conn.cursor()
    cur.execute("SELECT id, species, name, age, weight, arrival_date FROM animals ORDER BY id ASC;")
    rows = cur.fetchall()
    cur.close()
    return rows


def select_heavy_animals(
    conn: sqlite3.Connection, min_weight: float
) -> List[AnimalRow]:
    """Повертає тварин із вагою більшою за min_weight, відсортованих за спаданням ваги."""
    cur = conn.cursor()
    cur.execute(
        """
        SELECT id, species, name, age, weight, arrival_date
        FROM animals
        WHERE weight > ?
        ORDER BY weight DESC;
        """,
        (min_weight,),
    )
    rows = cur.fetchall()
    cur.close()
    return rows


def select_animals_by_species(
    conn: sqlite3.Connection, species: str
) -> List[AnimalRow]:
    """Повертає тварин певного виду, відсортованих за віком за зростанням."""
    cur = conn.cursor()
    cur.execute(
        """
        SELECT id, species, name, age, weight, arrival_date
        FROM animals
        WHERE species = ?
        ORDER BY age ASC;
        """,
        (species,),
    )
    rows = cur.fetchall()
    cur.close()
    return rows


def print_table(title: str, rows: List[AnimalRow]) -> None:
    """Форматовано виводить результати SELECT-запиту в консоль."""
    print(f"\n--- {title} ---")
    header = f"{'ID':<4} | {'Вид':<10} | {'Кличка':<12} | {'Вік':<5} | {'Вага (кг)':<10} | {'Дата прибуття':<12}"
    print(header)
    print("-" * len(header))
    for row in rows:
        print(
            f"{row[0]:<4} | {row[1]:<10} | {row[2]:<12} | {row[3]:<5} | {row[4]:<10.1f} | {row[5]:<12}"
        )


def main(db_path: str = DEFAULT_DB_PATH) -> None:
    """Головна функція демонстрації CRUD-операцій з базою даних «Ферма»."""
    conn = None
    try:
        conn = get_connection(db_path)
        print(f"Успішно підключено до бази даних «Ферма»: {db_path}")

        # Завдання 3: Створення таблиці «Тварини» (animals)
        create_animals_table(conn)
        reset_animals_table(conn)
        print("Таблицю 'animals' успішно створено та підготовлено до роботи.")

        # Завдання 4: Вставка принаймні 5 рядків даних
        initial_animals = [
            ("Корова", "Зірка", 4, 520.5, "2022-04-15"),
            ("Кінь", "Буран", 6, 480.0, "2021-06-10"),
            ("Вівця", "Хмаринка", 2, 65.3, "2024-03-20"),
            ("Свиня", "Пятачок", 1, 110.0, "2025-02-12"),
            ("Коза", "Білка", 3, 48.7, "2023-08-05"),
            ("Корова", "Квітка", 5, 545.2, "2021-09-18"),
        ]
        inserted = insert_animals(conn, initial_animals)
        print(f"Додано записів у таблицю 'animals': {inserted}")
        print_table("Початковий вміст таблиці 'animals'", select_all_animals(conn))

        # Завдання 5: Оновлення даних за умовою
        updated = update_animal_weight_and_age(conn, "Зірка", new_weight=538.0, new_age=5)
        print(f"\nОновлено записів (кличка = 'Зірка'): {updated}")

        # Завдання 6: Видалення даних за умовою
        deleted = delete_animal_by_name(conn, "Пятачок")
        print(f"Видалено записів (кличка = 'Пятачок'): {deleted}")

        # Завдання 7: Вибірка даних з умовами та сортуванням
        print_table("Усі тварини після оновлення та видалення", select_all_animals(conn))
        print_table(
            "Тварини з вагою понад 100 кг (сортування за спаданням ваги)",
            select_heavy_animals(conn, 100.0),
        )
        print_table(
            "Вибірка за видом 'Корова' (сортування за зростанням віку)",
            select_animals_by_species(conn, "Корова"),
        )

    except sqlite3.Error as error:
        print(f"Помилка під час роботи з базою даних SQLite: {error}")
    finally:
        if conn is not None:
            conn.close()
            print("\nЗ'єднання з базою даних закрито.")


if __name__ == "__main__":
    main()
