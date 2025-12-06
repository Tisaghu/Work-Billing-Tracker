# data_manager.py
from datetime import date
from src.models import WorkChunk, Day
from src.storage import load_chunks_from_csv, save_chunks_to_csv


class DataManager:
    """
    Represents a Data Management object for the Billing Tracker. Responsible for
    managing time chunks.

    Attributes:
        chunks(list): A list of all recorded time chunk objects. (See models.py)
        days_dict: A dictionary that sorts all recorded time chunk objects from
                   the chunks list by date.
    """
    def __init__(self):
        self.chunks = []
        self.days_dict = {}
        self.load_data()

    def load_data(self):
        """Load chunks from CSV and build day dictionary."""
        self.chunks = load_chunks_from_csv()
        self.days_dict = self._create_day_dict(self.chunks)

    def save_chunks(self, new_chunks, append=True):
        """Save chunks to CSV and reload local cache."""
        save_chunks_to_csv(new_chunks, append=append)
        self.load_data()

    def delete_chunk(self, chunk_id):
        """Delete a chunk by ID and persist changes."""
        self.chunks = [c for c in self.chunks if c.chunk_id != str(chunk_id)]
        self.save_chunks(self.chunks, append=False)

    def add_chunks(self, selected_date, minute_chunks, description):
        """Create and save new chunks for a date."""
        max_id = self.get_max_id()
        new_chunks = []

        for m in minute_chunks:
            max_id += 1
            new_chunks.append(
                WorkChunk(str(max_id), selected_date, m, description.strip())
            )

        self.save_chunks(new_chunks, append=True)

    def get_max_id(self):
        """Get highest existing chunk ID, or 0 if empty."""
        if self.chunks:
            return max(int(c.chunk_id) for c in self.chunks)
        return 0

    def _create_day_dict(self, chunks):
        """
        Build a dictionary of Day objects keyed by date.
        
        :param chunks: List of chunk objects to build dictionary.
        """
        days_dict = {}
        for chunk in chunks:
            if chunk.chunk_date not in days_dict:
                days_dict[chunk.chunk_date] = Day(chunk.chunk_date, [])
            days_dict[chunk.chunk_date].chunks.append(chunk)
        return days_dict

    def add_chunks_to_day(self, date, chunks):
        """
        Adds chunks from a list of chunks to a day object.
        
        :param date: Date for chunks to be added to.
        :param chunks: List of chunk objects to add to day.
        """
        if date not in self.days_dict:
            day_obj = Day(date, chunks)
            self.days_dict[date] = day_obj
            
        day_obj = self.days_dict[date]

        for chunk in chunks:
            day_obj.chunks.append(chunk)