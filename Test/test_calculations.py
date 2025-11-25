import pytest

from PyQt5.QtWidgets import QApplication
from src.calculations import *
from datetime import date

@pytest.fixture(scope="session")
def qapp():
    """Create QApplication once for all tests."""
    app = QApplication.instance()
    if app is None:
        app = QApplication([])
    return app

@pytest.fixture(autouse=True)
def use_qapp(qapp):
    """Automatically use qapp for every test."""
    pass

@pytest.mark.parametrize("input_date,expected_start,expected_end", [
    (date(2025, 9, 30), date(2025, 9, 29), date(2025, 10, 5)),  # Tuesday
    (date(2025, 10, 5), date(2025, 9, 29), date(2025, 10, 5)),  # Sunday
    (date(2025, 10, 6), date(2025, 10, 6), date(2025, 10, 12)), # Monday
    (date(2025, 12, 31), date(2025, 12, 29), date(2026, 1, 4)) # Into next year
])
def test_get_week_range(input_date, expected_start, expected_end):
    start, end = get_week_range(input_date)
    assert start == expected_start
    assert end == expected_end

@pytest.mark.parametrize("input_date,expected_start,expected_end", [
    (date(2025, 10, 15), date(2025, 10, 1), date(2025, 10, 31)),
    (date(2024, 2, 4), date(2024, 2, 1), date(2024, 2, 29)) # Leap Year
])
def test_get_month_range(input_date, expected_start, expected_end):
    start, end = get_month_range(input_date)
    assert start == expected_start
    assert end == expected_end
