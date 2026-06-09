"""
Тесты для программы подсчёта этажей (Вариант 17: Лифт Дилли)
=============================================================

Содержит:
  - Тесты «белого ящика»: unit-тесты для каждого модуля (функции).
  - Тесты «чёрного ящика»: интеграционные тесты по входным/выходным данным.

Запуск:
    python -m unittest tests/test_elevator.py -v
"""

import sys
import os
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from elevator import validate_input, simulate_elevator, calculate_floors, count_floors


# ─────────────────────────────────────────────────────────────────────────────
# ТЕСТЫ «БЕЛОГО ЯЩИКА» — модуль validate_input
# ─────────────────────────────────────────────────────────────────────────────

class TestValidateInput(unittest.TestCase):
    """Тесты модуля validate_input (проверка входных данных)."""

    def test_valid_only_ones(self):
        self.assertEqual(validate_input("11"), "11")

    def test_valid_only_twos(self):
        self.assertEqual(validate_input("22"), "22")

    def test_valid_mixed(self):
        self.assertEqual(validate_input("21212"), "21212")

    def test_valid_single_one(self):
        self.assertEqual(validate_input("1"), "1")

    def test_valid_single_two(self):
        self.assertEqual(validate_input("2"), "2")

    def test_valid_max_length(self):
        s = "12" * 50
        self.assertEqual(validate_input(s), s)

    def test_valid_complex(self):
        s = "1221221221221"
        self.assertEqual(validate_input(s), s)

    def test_empty_string_raises(self):
        with self.assertRaises(ValueError):
            validate_input("")

    def test_too_long_raises(self):
        with self.assertRaises(ValueError):
            validate_input("1" * 101)

    def test_invalid_digit_raises(self):
        with self.assertRaises(ValueError):
            validate_input("123")

    def test_space_raises(self):
        with self.assertRaises(ValueError):
            validate_input("1 2")

    def test_letter_raises(self):
        with self.assertRaises(ValueError):
            validate_input("1a2")

    def test_zero_raises(self):
        with self.assertRaises(ValueError):
            validate_input("102")

    def test_newline_raises(self):
        with self.assertRaises(ValueError):
            validate_input("1\n2")


# ─────────────────────────────────────────────────────────────────────────────
# ТЕСТЫ «БЕЛОГО ЯЩИКА» — модуль simulate_elevator
# ─────────────────────────────────────────────────────────────────────────────

class TestSimulateElevator(unittest.TestCase):
    """Тесты модуля simulate_elevator (симуляция движения лифта)."""

    def test_all_up(self):
        self.assertEqual(simulate_elevator("11"), (0, 2))

    def test_all_down(self):
        self.assertEqual(simulate_elevator("22"), (-2, 0))

    def test_alternating_start_down(self):
        self.assertEqual(simulate_elevator("21212"), (-1, 0))

    def test_single_up(self):
        self.assertEqual(simulate_elevator("1"), (0, 1))

    def test_single_down(self):
        self.assertEqual(simulate_elevator("2"), (-1, 0))

    def test_up_then_down(self):
        self.assertEqual(simulate_elevator("12"), (0, 1))

    def test_complex_sequence(self):
        min_p, max_p = simulate_elevator("1221221221221")
        self.assertEqual(min_p, -4)
        self.assertEqual(max_p, 1)

    def test_three_up(self):
        self.assertEqual(simulate_elevator("111"), (0, 3))

    def test_start_position_in_range(self):
        min_p, max_p = simulate_elevator("1")
        self.assertEqual(min_p, 0)   # начальная позиция = 0

# ─────────────────────────────────────────────────────────────────────────────
# ТЕСТЫ «БЕЛОГО ЯЩИКА» — модуль calculate_floors
# ─────────────────────────────────────────────────────────────────────────────

class TestCalculateFloors(unittest.TestCase):
    """Тесты модуля calculate_floors (вычисление количества этажей)."""

    def test_range_zero(self):
        self.assertEqual(calculate_floors(0, 0), 1)

    def test_range_one(self):
        self.assertEqual(calculate_floors(0, 1), 2)

    def test_range_two(self):
        self.assertEqual(calculate_floors(0, 2), 3)

    def test_negative_min(self):
        self.assertEqual(calculate_floors(-1, 0), 2)

    def test_both_sides(self):
        self.assertEqual(calculate_floors(-4, 1), 6)

    def test_only_negative(self):
        self.assertEqual(calculate_floors(-2, 0), 3)

    def test_large_range(self):
        self.assertEqual(calculate_floors(0, 99), 100)


# ─────────────────────────────────────────────────────────────────────────────
# ТЕСТЫ «ЧЁРНОГО ЯЩИКА» — count_floors (интеграционные)
# ─────────────────────────────────────────────────────────────────────────────

class TestCountFloors(unittest.TestCase):
    """Тесты «чёрного ящика» для count_floors."""

    # --- Примеры из условия ---
    def test_given_example_1(self):
        self.assertEqual(count_floors("11"), 3)

    def test_given_example_2(self):
        self.assertEqual(count_floors("21212"), 2)

    def test_given_example_3(self):
        self.assertEqual(count_floors("1221221221221"), 6)

    # --- Граничные случаи ---
    def test_single_up(self):
        self.assertEqual(count_floors("1"), 2)

    def test_single_down(self):
        self.assertEqual(count_floors("2"), 2)

    def test_max_length_all_up(self):
        self.assertEqual(count_floors("1" * 100), 101)

    # --- Дополнительные тесты ---
    def test_three_floors_simple(self):
        self.assertEqual(count_floors("1122"), 3)

    def test_two_floors_alternating(self):
        self.assertEqual(count_floors("1212"), 2)

    def test_zigzag_up(self):
        self.assertEqual(count_floors("11211"), 4)

    def test_explore_both_directions(self):
        self.assertEqual(count_floors("11222"), 4)

    def test_deep_descent(self):
        self.assertEqual(count_floors("22222"), 6)

    def test_two_floors_only(self):
        self.assertEqual(count_floors("12"), 2)

    def test_up_down_up(self):
        self.assertEqual(count_floors("121"), 2)

    # --- Некорректный ввод ---
    def test_invalid_empty(self):
        with self.assertRaises(ValueError):
            count_floors("")

    def test_invalid_bad_char(self):
        with self.assertRaises(ValueError):
            count_floors("1231")

    def test_invalid_too_long(self):
        with self.assertRaises(ValueError):
            count_floors("1" * 101)


if __name__ == "__main__":
    unittest.main(verbosity=2)
