# models.py
# Contains data models for the Work Billing Tracker

from datetime import date
from typing import List

class WorkChunk:
    """
    Represents a chunk of work (in minutes) billed to a specific date.
    """
    def __init__(self, chunk_date: date, minutes: int, description: str = ""):
        self.chunk_date = chunk_date
        self.minutes = minutes
        self.description = description

    def to_csv_row(self) -> List[str]:
        """Convert to a list of strings for CSV writing."""
        return [self.chunk_date.isoformat(), str(self.minutes), self.description]

    @staticmethod
    def from_csv_row(row: List[str]) -> 'WorkChunk':
        from datetime import datetime
        chunk_date = datetime.strptime(row[0], '%Y-%m-%d').date()
        minutes = int(row[1])
        description = row[2] if len(row) > 2 else ""
        return WorkChunk(chunk_date, minutes, description)
