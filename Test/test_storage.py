import pytest
from src.storage import save_chunks_to_csv, load_chunks_from_csv
from src.models import WorkChunk
from datetime import date

TEST_FILENAME = "test_work_chunks.csv"


def test_create_new_csv(tmp_path):
    test_file = tmp_path / TEST_FILENAME

    # Create test chunk
    chunk1 = WorkChunk("1", date(2025, 9, 30), 60, "Test 1")
    chunk2 = WorkChunk("2", date(2025,9, 30), 30, "Test 2")

    save_chunks_to_csv([chunk1, chunk2], filename=str(test_file), append=False)

    # Check that the file was created
    assert test_file.exists()

    # Check that the file is not empty
    assert test_file.stat().st_size > 0

    # Check that the header is present
    with open(test_file, "r", encoding="utf-8") as f:
        header = f.readline().strip()
        assert header == "ID,Date,Minutes,Description"

def test_load_no_file(tmp_path):
    test_file = tmp_path / "does_not_exist.csv"

    chunks = load_chunks_from_csv(str(test_file))

    assert chunks == []

def test_load_from_csv(tmp_path):
    test_file = tmp_path / TEST_FILENAME

    # Create test chunk
    chunk1 = WorkChunk("1", date(2025, 9, 30), 60, "Test 1")
    chunk2 = WorkChunk("2", date(2025,9, 30), 30, "Test 2")

    save_chunks_to_csv([chunk1, chunk2], filename=str(test_file), append=False)

    loaded_chunks = load_chunks_from_csv(str(test_file))

    assert len(loaded_chunks) == 2
    assert loaded_chunks[0].description == "Test 1"
    assert loaded_chunks[1].minutes == 30