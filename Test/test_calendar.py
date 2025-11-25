import pytest
from datetime import date
from unittest.mock import patch

from src.GUI.custom_calendar import *

@pytest.fixture
def calendar_instance():
    """Fixture to create a calendar instance for testing."""
    return CustomCalendarWidget()

def test_calendar_creation(calendar_instance):
    """Test that the calendar instantiates correctly."""
    assert calendar_instance is not None

def test_old_highlight_cleared_on_date_change(calendar_instance):
    """Test that the previous day's highlight is cleared when date rolls over."""
    # Get today and yesterday
    today = QDate.currentDate()
    yesterday = today.addDays(-1)

    # Simulate yesterday was highlighted
    calendar_instance._last_highlighted_date = yesterday

    # Mock QDate.currentDate() to return today
    with patch('src.GUI.custom_calendar.QDate.currentDate', return_value=today):
        # Trigger the date check
        calendar_instance._check_today_changed()

    # Verify today is now the highlighted date
    assert calendar_instance._last_highlighted_date == today

    # Verify yesterday has no formatting
    yesterday_format = calendar_instance.dateTextFormat(yesterday)
    assert yesterday_format.background().color().name() != "#444444"  # not weekend color
    assert yesterday_format.background().color().name() != "#F4F8A4"  # not today color    
