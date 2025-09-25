import sys
import calculations

from datetime import date

from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget,
    QVBoxLayout, QHBoxLayout, QCalendarWidget,
    QLabel, QPushButton, QListWidget,  QMessageBox,
)
from PyQt5.QtCore import QDate

from models import WorkChunk, Day
from storage import load_chunks_from_csv, save_chunks_to_csv
from stats_panel import StatsPanel
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

        # Main data — initially empty; refresh_entries function will reload from disk
        self.chunks = []
        self.days_dict = {}
        self.selected_date = date.today() #Set the selected date to today by default

        # --- Widgets ---
        self.central = QWidget()
        self.main_layout = QHBoxLayout()
        self.left_layout = QVBoxLayout()
        self.settings_layout = QHBoxLayout()
        self.right_layout = QVBoxLayout()

        # Create and connect calendar widget
        self.calendar = QCalendarWidget()
        self.calendar.setVerticalHeaderFormat(QCalendarWidget.NoVerticalHeader)
        self.calendar.setSelectedDate(QDate.currentDate())
        self.calendar.selectionChanged.connect(self.on_date_changed)

        # Create list to display entries on selected day
        self.entry_list = QListWidget()
        self.status_label = QLabel()

        # Create and connect buttons for editing and deleting entries
        self.edit_button = QPushButton("Edit Time Entry (WIP)")
        self.delete_button = QPushButton("Delete Selected Entry")
        self.edit_button.clicked.connect(self.edit_time_entry)
        self.delete_button.clicked.connect(self.delete_selected_entry)

        # Add widgets to left layout
        for widget in [
            self.calendar,
            self.status_label,
            self.entry_list,
            self.edit_button,
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
        
        # Set central layout
        self.central.setLayout(self.main_layout)
        self.setCentralWidget(self.central)

        # initialize the chunks list and days_dict from CSV file
        self.initialize_lists()

        # initial load of main GUI elements
        self.refresh_entries()


    def initialize_lists(self):
        """Load the time chunks from the CSV file into the chunks list, and build the day dictionary 
            using the chunks list. """
        self.chunks = load_chunks_from_csv()
        self.days_dict = self.create_day_dict(self.chunks)

    def on_date_changed(self):
        """Update the calendar, selected_date variable, and entries for the newly selected date."""
        qdate = self.calendar.selectedDate()
        self.selected_date = qdate.toPyDate()
        self.refresh_entries()

    def refresh_entries(self):
        """Reload chunks from disk (CSV) and update the entries list + stats."""
        from calculations import get_week_range, get_month_range, get_weekdays_in_range

        # clear UI list and compute stats
        self.entry_list.clear()
        count_for_selected_date = 0
        billed_today = 0
        billed_week = 0
        billed_month = 0

        #today = date.today()
        week_start, week_end = get_week_range(self.selected_date)
        month_start, month_end = get_month_range(self.selected_date)

        # Show entries for the currently selected date
        if self.selected_date in self.days_dict:
            day_obj = self.days_dict[self.selected_date]
            for chunk in day_obj.chunks:
                self.entry_list.addItem(f"ID:{chunk.chunk_id}, {chunk.minutes} min - {chunk.description}")
                count_for_selected_date += 1

        #TODO: Organize these better 
        billed_today = calculations.get_total_minutes_for_day(self.chunks, self.selected_date)
        billed_week = StatsPanel.calculate_billed_time(self.selected_date, "week", self.chunks)
        billed_month = StatsPanel.calculate_billed_time(self.selected_date, "month", self.chunks)

        self.status_label.setText(f"Entries for {self.selected_date} ({count_for_selected_date}):")

        # Calculate goals
        today_goal = DAILY_GOAL
        week_goal = DAILY_GOAL * len(get_weekdays_in_range(week_start, week_end))
        month_goal = DAILY_GOAL * len(get_weekdays_in_range(month_start, month_end))

        # Update the right-hand stats panel
        self.stats_panel.update_stats(
            billed_today, billed_week, billed_month,
            today_goal, week_goal, month_goal
        )

    def edit_time_entry(self):
        pass

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

                #Refresh chunk and day lists and refresh GUI
                self.initialize_lists()
                self.refresh_entries()
                return
                
    def handle_add_time_panel_done(self, minute_chunks, description):
        if not minute_chunks:
            return
        
        #get max id from existing chunks
        max_id = self.find_max_id()
        new_chunks = []
        
        # Build new chunks
        new_chunks = self.build_new_chunk_list(max_id, self.selected_date, minute_chunks, description)

        # Save new chunks to CSV
        save_chunks_to_csv(new_chunks, append=True)
        self.add_chunks_to_day(self.selected_date, new_chunks)
        self.refresh_entries()

    def add_chunks_to_day(self, date, chunks):
        if date not in self.days_dict:
            day_obj = Day(date, chunks)
            self.days_dict[date] = day_obj
        else:
            day_obj = self.days_dict[date]
            for chunk in chunks:
                day_obj.chunks.append(chunk)



    def find_max_id(self):
        existing_chunks = load_chunks_from_csv()
        if existing_chunks:
            max_id = max(int(c.chunk_id) for c in existing_chunks)
        else:
            max_id = 0
        return max_id
    
    
    def build_new_chunk_list(self, max_id, selected_date, minute_chunks, description):
        new_chunks = []
        for m in minute_chunks:
            max_id += 1
            new_chunks.append(WorkChunk(str(max_id),selected_date, m, description.strip()))
        
        return new_chunks
    
    def create_day_dict(self, chunks):
        days_dict = {}

        for chunk in chunks:
            if chunk.chunk_date not in days_dict:
                day_obj = Day(chunk.chunk_date, [])
                day_obj.chunks.append(chunk)
                days_dict[chunk.chunk_date] = day_obj
            else:
                day_obj = days_dict[chunk.chunk_date]
                day_obj.chunks.append(chunk)

        return days_dict



def run_gui():
    app = QApplication(sys.argv)
    window = BillingTrackerGUI()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    run_gui()
