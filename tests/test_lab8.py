"""
Юніт-тести для Лабораторної роботи № 8 (Варіант 11: база даних «Ферма», таблиця animals).
"""
import sqlite3
import unittest

from src.lab8 import (
    create_animals_table,
    delete_animal_by_name,
    insert_animals,
    select_all_animals,
    select_animals_by_species,
    select_heavy_animals,
    update_animal_weight_and_age,
)


class TestLab8FarmDatabase(unittest.TestCase):
    """Перевірка всіх CRUD-операцій з таблицею animals в оперативній БД SQLite."""

    def setUp(self):
        self.conn = sqlite3.connect(":memory:")
        create_animals_table(self.conn)
        self.sample_data = [
            ("Корова", "Зірка", 4, 520.5, "2022-04-15"),
            ("Кінь", "Буран", 6, 480.0, "2021-06-10"),
            ("Вівця", "Хмаринка", 2, 65.3, "2024-03-20"),
            ("Свиня", "Пятачок", 1, 110.0, "2025-02-12"),
            ("Коза", "Білка", 3, 48.7, "2023-08-05"),
        ]
        insert_animals(self.conn, self.sample_data)

    def tearDown(self):
        self.conn.close()

    def test_insert_and_select_all(self):
        """Перевірка вставки 5 рядків та вибірки всіх даних."""
        rows = select_all_animals(self.conn)
        self.assertEqual(len(rows), 5)
        self.assertEqual(rows[0][2], "Зірка")

    def test_update_animal(self):
        """Перевірка оновлення ваги та віку тварини."""
        updated = update_animal_weight_and_age(self.conn, "Зірка", 540.0, 5)
        self.assertEqual(updated, 1)
        cows = select_animals_by_species(self.conn, "Корова")
        self.assertEqual(cows[0][3], 5)
        self.assertAlmostEqual(cows[0][4], 540.0)

    def test_delete_animal(self):
        """Перевірка видалення запису за кличкою."""
        deleted = delete_animal_by_name(self.conn, "Пятачок")
        self.assertEqual(deleted, 1)
        self.assertEqual(len(select_all_animals(self.conn)), 4)

    def test_select_heavy_animals_sorted(self):
        """Перевірка фільтрації за вагою та сортування за спаданням."""
        heavy = select_heavy_animals(self.conn, 100.0)
        self.assertEqual(len(heavy), 3)
        weights = [row[4] for row in heavy]
        self.assertEqual(weights, sorted(weights, reverse=True))


if __name__ == "__main__":
    unittest.main()
