# calculations.py
# Business logic for the Work Billing Tracker (totals, week/month logic, etc.)

import calendar
from datetime import date, timedelta
from typing import List
from models import WorkChunk

def get_week_range(target_date: date):
    """
    Returns the start (Monday) and end (Sunday) date of the week containing target_date.
    """
    start = target_date - timedelta(days=target_date.weekday())  # Monday
    end = start + timedelta(days=6)  # Sunday
    return start, end

def get_month_range(target_date: date):
    """
    Returns the first and last date of the month containing target_date.
    """
    first = target_date.replace(day=1)
    last_day = calendar.monthrange(target_date.year, target_date.month)[1]
    last = target_date.replace(day=last_day)
    return first, last

def get_weekdays_in_range(start_date: date, end_date: date) -> List[date]:
    """
    Returns a list of all weekdays (Mon-Fri) between start_date and end_date, inclusive.
    """
    days = []
    current = start_date
    while current <= end_date:
        if current.weekday() < 5:  # 0=Mon, 4=Fri
            days.append(current)
        current += timedelta(days=1)
    return days

def get_total_minutes_for_range(chunks: List[WorkChunk], start_date: date, end_date: date) -> int:
    """
    Sums all minutes for entries between start_date and end_date, inclusive.
    """
    return sum(chunk.minutes for chunk in chunks if start_date <= chunk.chunk_date <= end_date)

def get_total_minutes_for_day(chunks: List[WorkChunk], target_date: date) -> int:
    """
    Sum all minutes for a specific date.
    """
    #TODO: Can probably refactor this using the day_dict instead of the chunk list
    return sum(chunk.minutes for chunk in chunks if chunk.chunk_date == target_date)
