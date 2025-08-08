# gui_app.py
import sys
from datetime import date, datetime, timedelta

from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget,
    QVBoxLayout, QHBoxLayout, QCalendarWidget,
    QLabel, QPushButton, QListWidget, QInputDialog, QMessageBox,
    QDialog, QLineEdit
)
from PyQt5.QtCore import QDate, Qt

from models import WorkChunk
from storage import load_chunks_from_csv, save_chunks_to_csv

# Constants
DAILY_GOAL = 480  # minutes per workday


class StatsPanel(QWidget):
    def __init__(self):
        super().__init__()

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        # Create labels for each stat and store them for easy updates
        self.billed_today_label = QLabel("Billed today: 0 min")
        self.billed_week_label = QLabel("Billed this week: 0 min")
        self.billed_month_label = QLabel("Billed this month: 0 min")
        self.goal_percent_label = QLabel("Weekly goal completion: 0%")
        self.minutes_remaining_label = QLabel("Minutes remaining: 0")

        # Make them look neat
        for lbl in [
            self.billed_today_label,
            self.billed_week_label,
            self.billed_month_label,
            self.goal_percent_label,
            self.minutes_remaining_label
        ]:
            lbl.setAlignment(Qt.AlignLeft)
            self.layout.addWidget(lbl)

        self.layout.addStretch()  # Push everything up

    def update_stats(self, billed_today, billed_week, billed_month, weekly_goal_minutes):
        """Update stats dynamically from your main app.

        Note: weekly percentage is calculated from billed_week / weekly_goal_minutes.
        """
        self.billed_today_label.setText(f"Billed today: {billed_today} min")
        self.billed_week_label.setText(f"Billed this week: {billed_week} min")
        self.billed_month_label.setText(f"Billed this month: {billed_month} min")

        if weekly_goal_minutes > 0:
            percent = (billed_week / weekly_goal_minutes) * 100
            remaining = weekly_goal_minutes - billed_week
        else:
            percent = 0
            remaining = 0

        self.goal_percent_label.setText(f"Weekly goal completion: {percent:.1f}%")
        self.minutes_remaining_label.setText(f"Minutes remaining: {max(0, remaining)}")


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
        self.resize(900, 600)
        self.stats_panel = StatsPanel()

        # Main data — initially empty; refresh_entries will reload from disk
        self.chunks = []
        self.current_date = date.today()

        # --- Widgets ---
        self.central = QWidget()
        self.main_layout = QHBoxLayout()
        self.left_layout = QVBoxLayout()

        self.calendar = QCalendarWidget()
        self.calendar.setSelectedDate(QDate.currentDate())
        self.calendar.selectionChanged.connect(self.on_date_changed)

        self.entry_list = QListWidget()
        self.status_label = QLabel()

        self.add_button = QPushButton("Add Time Entry")
        self.delete_button = QPushButton("Delete Selected Entry")

        self.add_button.clicked.connect(self.add_time_entry)
        self.delete_button.clicked.connect(self.delete_selected_entry)

        # Add widgets to left layout
        self.left_layout.addWidget(self.calendar)
        self.left_layout.addWidget(self.status_label)
        self.left_layout.addWidget(self.entry_list)
        self.left_layout.addWidget(self.add_button)
        self.left_layout.addWidget(self.delete_button)

        # Add left and right (stats) panels to main layout
        self.main_layout.addLayout(self.left_layout, stretch=3)
        self.main_layout.addWidget(self.stats_panel, stretch=1)

        self.central.setLayout(self.main_layout)
        self.setCentralWidget(self.central)

        # initial load
        self.refresh_entries()

    def on_date_changed(self):
        qdate = self.calendar.selectedDate()
        self.current_date = qdate.toPyDate()
        self.refresh_entries()

    def refresh_entries(self):
        """Reload chunks from disk (CSV) and update the entries list + stats."""
        # reload authoritative data from CSV via your storage helper
        # this ensures GUI always reflects the file on disk (single source of truth)
        self.chunks = load_chunks_from_csv()

        # clear UI list and compute stats
        self.entry_list.clear()
        count_for_selected_date = 0
        billed_today = 0
        billed_week = 0
        billed_month = 0

        today = date.today()
        # Monday is weekday() == 0. Work week is Mon-Fri -> week_end = Monday + 4 days
        week_start = today - timedelta(days=today.weekday())
        week_end = week_start + timedelta(days=4)

        for chunk in self.chunks:
            # chunk.chunk_date expected to be a date object (from load_chunks_from_csv)
            # show entries for currently selected date (left list)
            if chunk.chunk_date == self.current_date:
                self.entry_list.addItem(f"{chunk.minutes} min - {chunk.description}")
                count_for_selected_date += 1

            # accumulate stats (always compare to today's date for "today/week/month")
            if chunk.chunk_date == today:
                billed_today += chunk.minutes
            if week_start <= chunk.chunk_date <= week_end:
                billed_week += chunk.minutes
            if chunk.chunk_date.year == today.year and chunk.chunk_date.month == today.month:
                billed_month += chunk.minutes

        self.status_label.setText(f"Entries for {self.current_date} ({count_for_selected_date}):")

        # Weekly goal (5 workdays)
        weekly_goal = DAILY_GOAL * 5

        # Update the right-hand stats panel
        self.stats_panel.update_stats(billed_today, billed_week, billed_month, weekly_goal)

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

        # Make sure we have the latest data from disk before appending
        self.chunks = load_chunks_from_csv()

        for m in minute_chunks:
            self.chunks.append(WorkChunk(self.current_date, m, desc.strip()))
        save_chunks_to_csv(self.chunks)

        # reload from disk and refresh UI/stats
        self.refresh_entries()

    def delete_selected_entry(self):
        selected_items = self.entry_list.selectedItems()
        if not selected_items:
            QMessageBox.information(self, "No selection", "Select an entry to delete.")
            return

        selected_text = selected_items[0].text()
        minutes_str, _, desc = selected_text.partition(" min - ")
        try:
            minutes = int(minutes_str.strip())
        except ValueError:
            QMessageBox.warning(self, "Parse error", "Couldn't parse selected entry.")
            return

        # Reload authoritative chunks from disk to ensure sync
        self.chunks = load_chunks_from_csv()

        # Find matching chunk (first match)
        for i, chunk in enumerate(self.chunks):
            if chunk.chunk_date == self.current_date and chunk.minutes == minutes and chunk.description == desc:
                del self.chunks[i]
                save_chunks_to_csv(self.chunks)
                self.refresh_entries()
                return

        QMessageBox.information(self, "Not found", "Matching entry not found in CSV.")

def run_gui():
    app = QApplication(sys.argv)
    window = BillingTrackerGUI()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    run_gui()
