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

from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QLineEdit, QPushButton,
    QLabel, QListWidget, QHBoxLayout
)

class AddTimeDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Add Time Chunks")
        self.resize(300, 300)

        self.minutes = []

        self.layout = QVBoxLayout()
        self.input_field = QLineEdit()
        self.input_field.setPlaceholderText("Enter minutes and press Add or Enter")
        self.chunk_list = QListWidget()

        self.add_button = QPushButton("Add")
        self.clear_button = QPushButton("Clear")
        self.done_button = QPushButton("Done")

        btn_layout = QHBoxLayout()
        btn_layout.addWidget(self.add_button)
        btn_layout.addWidget(self.clear_button)
        btn_layout.addWidget(self.done_button)

        self.layout.addWidget(QLabel("Enter time chunks (in minutes):"))
        self.layout.addWidget(self.input_field)
        self.layout.addWidget(self.chunk_list)
        self.layout.addLayout(btn_layout)
        self.setLayout(self.layout)

        # Connect buttons and input field
        self.add_button.clicked.connect(self.add_chunk)
        self.clear_button.clicked.connect(self.clear_chunks)
        self.done_button.clicked.connect(self.accept)
        self.input_field.returnPressed.connect(self.add_chunk)

    def add_chunk(self):
        text = self.input_field.text().strip()
        if not text:
            return
        try:
            minutes = int(text)
            if minutes <= 0:
                raise ValueError
        except ValueError:
            self.input_field.setText("")
            self.input_field.setPlaceholderText("Invalid! Enter a positive number")
            return

        self.minutes.append(minutes)
        self.chunk_list.addItem(f"{minutes} min")
        self.input_field.clear()

    def clear_chunks(self):
        self.minutes.clear()
        self.chunk_list.clear()

    def get_minutes(self):
        return self.minutes


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
        dialog = AddTimeDialog()
        if dialog.exec_() != QDialog.Accepted:
            return

        minute_chunks = dialog.get_minutes()
        if not minute_chunks:
            return

        desc, ok = QInputDialog.getText(self, "Description", "Optional description:")
        if not ok:
            return

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
