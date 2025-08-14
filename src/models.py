# models.py
# Contains data models for the Work Billing Tracker

from datetime import date
from typing import List

class WorkChunk:
    """
    Represents a chunk of work (in minutes) billed to a specific date.
    """
    def __init__(self,chunk_id:int, chunk_date: date, minutes: int, description: str = ""):
        self.chunk_id = chunk_id
        self.chunk_date = chunk_date
        self.minutes = minutes
        self.description = description

    def to_csv_row(self) -> List[str]:
        """Convert to a list of strings for CSV writing."""
        return [str(self.chunk_id), self.chunk_date.isoformat(), str(self.minutes), self.description]

    @staticmethod
    def from_csv_row(row: List[str]) -> 'WorkChunk':
        from datetime import datetime
        chunk_id = row[0]
        chunk_date = datetime.strptime(row[1], '%Y-%m-%d').date()
        minutes = int(row[2])
        description = row[3] if len(row) > 2 else ""
        return WorkChunk(chunk_id, chunk_date, minutes, description)
