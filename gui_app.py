import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget,
    QVBoxLayout, QCalendarWidget, QLabel,
    QPushButton, QListWidget, QInputDialog, QMessageBox
)
from PyQt5.QtCore import QDate
from datetime import date

from models import WorkChunk
from storage import load_chunks_from_csv, save_chunks_to_csv

class BillingTrackerGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Work Billing Tracker")
        self.resize(500, 600)

        # Main data
        self.chunks = load_chunks_from_csv()
        self.current_date = date.today()

        # --- Widgets ---
        self.central = QWidget()
        self.layout = QVBoxLayout()

        self.calendar = QCalendarWidget()
        self.calendar.setSelectedDate(QDate.currentDate())
        self.calendar.selectionChanged.connect(self.on_date_changed)

        self.entry_list = QListWidget()
        self.status_label = QLabel()

        self.add_button = QPushButton("Add Time Entry")
        self.delete_button = QPushButton("Delete Selected Entry")

        self.add_button.clicked.connect(self.add_time_entry)
        self.delete_button.clicked.connect(self.delete_selected_entry)

        # Add widgets to layout
        self.layout.addWidget(self.calendar)
        self.layout.addWidget(self.status_label)
        self.layout.addWidget(self.entry_list)
        self.layout.addWidget(self.add_button)
        self.layout.addWidget(self.delete_button)

        self.central.setLayout(self.layout)
        self.setCentralWidget(self.central)

        self.refresh_entries()

    def on_date_changed(self):
        qdate = self.calendar.selectedDate()
        self.current_date = qdate.toPyDate()
        self.refresh_entries()

    def refresh_entries(self):
        self.entry_list.clear()
        count = 0
        for chunk in self.chunks:
            if chunk.chunk_date == self.current_date:
                self.entry_list.addItem(f"{chunk.minutes} min - {chunk.description}")
                count += 1
        self.status_label.setText(f"Entries for {self.current_date} ({count}):")

    def add_time_entry(self):
        text, ok = QInputDialog.getText(self, "Add Time", "Enter minutes (e.g. 20+30+15):")
        if not ok or not text.strip():
            return

        try:
            minute_chunks = [int(m.strip()) for m in text.split('+')]
            if any(m <= 0 for m in minute_chunks):
                raise ValueError("Minutes must be positive.")
        except Exception as e:
            QMessageBox.critical(self, "Invalid Input", f"Error: {e}")
            return

        desc, _ = QInputDialog.getText(self, "Description", "Optional description:")
        for m in minute_chunks:
            self.chunks.append(WorkChunk(self.current_date, m, desc.strip()))
        save_chunks_to_csv(self.chunks)
        self.refresh_entries()

    def delete_selected_entry(self):
        selected_items = self.entry_list.selectedItems()
        if not selected_items:
            QMessageBox.information(self, "No selection", "Select an entry to delete.")
            return

        selected_text = selected_items[0].text()
        minutes, _, desc = selected_text.partition(" min - ")
        minutes = int(minutes.strip())

        # Find matching chunk (first match only)
        for i, chunk in enumerate(self.chunks):
            if chunk.chunk_date == self.current_date and chunk.minutes == minutes and chunk.description == desc:
                del self.chunks[i]
                save_chunks_to_csv(self.chunks)
                self.refresh_entries()
                return

def run_gui():
    app = QApplication(sys.argv)
    window = BillingTrackerGUI()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    run_gui()
