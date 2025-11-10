import src.calculations

from datetime import date

from PyQt5.QtWidgets import (
    QMainWindow, QWidget,
    QVBoxLayout, QHBoxLayout, QCalendarWidget,
    QLabel, QPushButton, QListWidget,  QMessageBox,
)
from PyQt5.QtCore import QDate, Qt

from PyQt5.QtGui import QTextCharFormat, QColor

from src.models import WorkChunk, Day
from src.storage import load_chunks_from_csv, save_chunks_to_csv
from src.calculations import *
from src.data_manager import DataManager
from src.GUI.Panels.stats_panel import StatsPanel
from src.GUI.Panels.add_time_panel import AddTimePanel
from src.GUI.custom_calendar import CustomCalendarWidget


# Constants
DAILY_GOAL = 480  # minutes per workday - (Assumes a standard 8 hours - need to account for lunches in the future)


class BillingTrackerGUI(QMainWindow):
#---------- INITIALIZATION ----------
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Work Billing Tracker")
        self.resize(900, 600)

        # Initialize widgets
        self.stats_panel = StatsPanel()
        self.add_time_panel = AddTimePanel(on_done_callback=self.handle_add_time_panel_done)

        # Main data — initially empty; initialize_lists function will reload from disk
        self.data_manager = DataManager()
        self.selected_date = date.today() #Set the selected date to today by default

        # --- Widgets ---
        self.central = QWidget()
        self.main_layout = QHBoxLayout()
        self.left_layout = QVBoxLayout()
        self.settings_layout = QHBoxLayout()
        self.right_layout = QVBoxLayout()

        # Calendar Widget Setup
        self.calendar = CustomCalendarWidget()
        self.calendar.setSelectedDate(QDate.currentDate())
        self.last_valid_date = self.calendar.selectedDate()
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

        # initial load of main GUI elements
        self.refresh_entries()


# ------------ EVENT HANDLERS ------------

    def on_date_changed(self):
        """Update the calendar, selected_date variable, and entries for the newly selected date."""
        qdate = self.calendar.selectedDate()
        if qdate.dayOfWeek() in (6, 7): # Saturday=6, Sunday=7
            # Revert to the last valid date
            self.calendar.setSelectedDate(self.last_valid_date)
        else:
            self.selected_date = qdate.toPyDate()
            self.last_valid_date = qdate
            self.refresh_entries()

    def edit_time_entry(self):
        pass


    def delete_selected_entry(self):
        selected_items = self.entry_list.selectedItems()
        if not selected_items:
            QMessageBox.information(self, "No selection", "Select an entry to delete.")
            return

        selected_text = selected_items[0].text()
        id_to_delete = int(selected_text.split(',')[0].split(':')[1])

        self.data_manager.delete_chunk(id_to_delete)
        self.refresh_entries()


#---------- CORE LOGIC ----------


    def refresh_entries(self):
        """Reload chunks from disk (CSV) and update the entries list + stats."""
        #from src.calculations import get_week_range, get_month_range, get_weekdays_in_range, calculate_billed_time
        

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
        if self.selected_date in self.data_manager.days_dict:
            day_obj = self.data_manager.days_dict[self.selected_date]
            for chunk in day_obj.chunks:
                self.entry_list.addItem(f"ID:{chunk.chunk_id}, {chunk.minutes} min - {chunk.description}")
                count_for_selected_date += 1
                billed_today += chunk.minutes
        else:
            # No day object for this day yet
            # TODO: need to alter how much I rely on the days_dict vs the chunks list for truth
            pass

        #TODO: Organize these better 
        billed_week = calculate_billed_time(self.selected_date, "week", self.data_manager.chunks)
        billed_month = calculate_billed_time(self.selected_date, "month", self.data_manager.chunks)

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

          
    def handle_add_time_panel_done(self, minutes, description):
        if not minutes:
            return
        
        #get max id from existing chunks
        max_id = self.data_manager.get_max_id()
        new_chunks = []
        
        # Build new chunks
        new_chunk = self.build_new_chunk(max_id, self.selected_date, minutes, description)
        new_chunks = [new_chunk]

        # Save new chunks to CSV
        save_chunks_to_csv(new_chunks, append=True)

        # Reinitialize lists and refresh entries to reflect changes
        self.data_manager.load_data()
        self.refresh_entries()    
        
    def build_new_chunk(self, max_id, selected_date, minutes, description):
        new_chunk = WorkChunk(str(max_id), selected_date, minutes, description.strip())
        return new_chunk
    
    def build_new_chunk_list(self, max_id, selected_date, minute_chunks, description):
        new_chunks = []
        for m in minute_chunks:
            max_id += 1
            new_chunks.append(WorkChunk(str(max_id),selected_date, m, description.strip()))
        
        return new_chunks
    
