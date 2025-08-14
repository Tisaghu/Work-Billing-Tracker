# storage.py
# Handles saving and loading data for the Work Billing Tracker

import csv
import os
from typing import List
from models import WorkChunk

FILENAME = 'work_chunks.csv'

def save_chunks_to_csv(chunks: List[WorkChunk], filename: str = FILENAME, append: bool = True):
    """Append or overwrite chunks in the CSV file, assigning IDs automatically if needed."""
    if append:
        # APPEND MODE
        file_exists = os.path.exists(filename)
        last_id = 0
        if file_exists:
            with open(filename, mode='r', newline='', encoding='utf-8') as f:
                reader = csv.reader(f)
                next(reader, None)
                for row in reader:
                    try:
                        last_id = int(row[0])
                    except (ValueError, IndexError):
                        pass

        with open(filename, mode='a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            if not file_exists:
                writer.writerow(['ID', 'Date', 'Minutes', 'Description'])

            for chunk in chunks:
                last_id += 1
                chunk.chunk_id = last_id
                writer.writerow(chunk.to_csv_row())

    else:
        # OVERWRITE MODE — always reassign IDs from 1..n
        with open(filename, mode='w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['ID', 'Date', 'Minutes', 'Description'])
            next_id = 1
            for chunk in chunks:
                chunk.chunk_id = next_id
                next_id += 1
                writer.writerow(chunk.to_csv_row())


def load_chunks_from_csv(filename: str = FILENAME) -> List[WorkChunk]:
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
