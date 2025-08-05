# storage.py
# Handles saving and loading data for the Work Billing Tracker

import csv
from typing import List
from models import WorkChunk

def save_chunks_to_csv(chunks: List[WorkChunk], filename: str = 'work_chunks.csv'):
    """Save all work chunks to a CSV file."""
    with open(filename, mode='w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['Date', 'Minutes', 'Description'])
        for chunk in chunks:
            writer.writerow(chunk.to_csv_row())

def load_chunks_from_csv(filename: str = 'work_chunks.csv') -> List[WorkChunk]:
    """Load all work chunks from a CSV file."""
    chunks = []
    try:
        with open(filename, mode='r', newline='', encoding='utf-8') as f:
            reader = csv.reader(f)
            next(reader)  # Skip header
            for row in reader:
                chunks.append(WorkChunk.from_csv_row(row))
    except FileNotFoundError:
        pass  # No data yet
    return chunks
