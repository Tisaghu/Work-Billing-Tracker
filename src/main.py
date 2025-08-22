import sys
from datetime import date

from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget,
    QVBoxLayout, QHBoxLayout, QCalendarWidget,
    QLabel, QPushButton, QListWidget, QInputDialog, QMessageBox,
    QDialog
)
from PyQt5.QtCore import QDate

from models import WorkChunk
from storage import load_chunks_from_csv, save_chunks_to_csv
from stats_panel import StatsPanel
from add_time_dialog import AddTimeDialog
from add_time_panel import AddTimePanel

# Constants
DAILY_GOAL = 480  # minutes per workday - (Assumes a standard 8 hours - need to account for lunches in the future)


class BillingTrackerGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Work Billing Tracker")
        self.resize(900, 600)

        # Initialize widgets
        self.stats_panel = StatsPanel()
        self.add_time_panel = AddTimePanel(on_done_callback=self.handle_add_time_panel_done)

        # Main data — initially empty; refresh_entries will reload from disk
        self.chunks = []
        self.current_date = date.today()

        # --- Widgets ---
        self.central = QWidget()
        self.main_layout = QHBoxLayout()
        self.left_layout = QVBoxLayout()
        self.right_layout = QVBoxLayout()

        # Create calendar widget
        self.calendar = QCalendarWidget()
        self.calendar.setSelectedDate(QDate.currentDate())
        self.calendar.selectionChanged.connect(self.on_date_changed)

        # Create list to display entries on selected day
        self.entry_list = QListWidget()
        self.status_label = QLabel()

        self.add_button = QPushButton("Add Time Entry")
        self.delete_button = QPushButton("Delete Selected Entry")

        self.add_button.clicked.connect(self.add_time_entry)
        self.delete_button.clicked.connect(self.delete_selected_entry)

        # Add widgets to left layout
        for widget in [
            self.calendar,
            self.status_label,
            self.entry_list,
            self.add_button,
            self.delete_button
        ]:
            self.left_layout.addWidget(widget)

        # Add widgets to right layout
        for widget in [
            self.stats_panel,
            self.add_time_panel
        ]:
            self.right_layout.addWidget(widget)

        # Add left and right (stats) panels to main layout
        self.main_layout.addLayout(self.left_layout, stretch=3)
        self.main_layout.addLayout(self.right_layout, stretch=1)
        #self.main_layout.addWidget(self.stats_panel, stretch=1)
        
        # Set central layout
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
        from calculations import get_week_range, get_month_range, get_weekdays_in_range

        self.chunks = load_chunks_from_csv()

        # clear UI list and compute stats
        self.entry_list.clear()
        count_for_selected_date = 0
        billed_today = 0
        billed_week = 0
        billed_month = 0

        today = date.today()
        week_start, week_end = get_week_range(today)
        month_start, month_end = get_month_range(today)

        for chunk in self.chunks:
            # chunk.chunk_date expected to be a date object (from load_chunks_from_csv)
            # show entries for currently selected date (left list)
            if chunk.chunk_date == self.current_date:
                self.entry_list.addItem(f"ID:{chunk.chunk_id}, {chunk.minutes} min - {chunk.description}")
                count_for_selected_date += 1

            # accumulate stats (always compare to today's date for "today/week/month")
            if chunk.chunk_date == today:
                billed_today += chunk.minutes
            if week_start <= chunk.chunk_date <= week_end:
                billed_week += chunk.minutes
            if month_start <= chunk.chunk_date <= month_end:
                billed_month += chunk.minutes

        self.status_label.setText(f"Entries for {self.current_date} ({count_for_selected_date}):")

        # Calculate goals
        today_goal = DAILY_GOAL
        week_goal = DAILY_GOAL * len(get_weekdays_in_range(week_start, week_end))
        month_goal = DAILY_GOAL * len(get_weekdays_in_range(month_start, month_end))

        # Update the right-hand stats panel
        self.stats_panel.update_stats(
            billed_today, billed_week, billed_month,
            today_goal, week_goal, month_goal
        )

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

        # Find max ID of existing chunks to assign ID of new chunks
        max_id = self.find_max_id()

        # Build *only* the new chunks
        # new_chunks = []
        # for m in minute_chunks:
        #     max_id += 1
        #     new_chunks.append(WorkChunk(str(max_id),self.current_date, m, desc.strip()))
        
        # Build *only* the new chunks
        new_chunks = self.build_new_chunk_list(max_id, self.current_date, minute_chunks, desc.strip())

        # Append these new chunks to the CSV
        save_chunks_to_csv(new_chunks, append=True)

        # Refresh UI from disk
        self.refresh_entries()

    def delete_selected_entry(self):
        selected_items = self.entry_list.selectedItems()
        if not selected_items:
            QMessageBox.information(self, "No selection", "Select an entry to delete.")
            return

        selected_text = selected_items[0].text()
        id_to_delete = int(selected_text.split(',')[0].split(':')[1])

        # Reload authoritative chunks from disk
        self.chunks = load_chunks_from_csv()

        # Find matching chunk (first match)
        for i, chunk in enumerate(self.chunks):
            if chunk.chunk_id == str(id_to_delete):
                del self.chunks[i]

                #Overwrite file with updated chunk list (no duplicates)
                save_chunks_to_csv(self.chunks, append=False)
                self.refresh_entries()
                return
                
    def handle_add_time_panel_done(self, minute_chunks, description):
        if not minute_chunks:
            return
        
        #get max id from existing chunks
        max_id = self.find_max_id()
        new_chunks = []
        
        # Build new chunks
        new_chunks = self.build_new_chunk_list(max_id, self.current_date, minute_chunks, description.strip())

        # Save new chunks to CSV
        save_chunks_to_csv(new_chunks, append=True)
        self.refresh_entries()

    def find_max_id(self):
        existing_chunks = load_chunks_from_csv()
        if existing_chunks:
            max_id = max(int(c.chunk_id) for c in existing_chunks)
        else:
            max_id = 0
        return max_id
    
    def build_new_chunk_list(self, max_id, current_date, minute_chunks, description):
        new_chunks = []
        for m in minute_chunks:
            max_id += 1
            new_chunks.append(WorkChunk(str(max_id),current_date, m, description.strip()))
        
        return new_chunks

def run_gui():
    app = QApplication(sys.argv)
    window = BillingTrackerGUI()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    run_gui()
