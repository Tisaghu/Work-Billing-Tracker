import pytest
from datetime import date

from src.models import WorkChunk, Day

def test_to_csv_row():
    test_date = date(2025, 9, 30)
    test_chunk = WorkChunk(1, test_date, 10, "Test")
    result = test_chunk.to_csv_row()
    expected = ["1",test_date.isoformat(),"10", "Test"]
    assert result == expected

def test_from_csv_row():
    pass