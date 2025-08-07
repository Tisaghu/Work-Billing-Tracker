import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QCalendarWidget, QPushButton, QLabel
from PyQt5.QtCore import QDate

class CalendarPicker(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Select a Date")
        self.resize(400,300)

        self.layout=QVBoxLayout()
        self.calendar = QCalendarWidget()
        self.label = QLabel("Selected Date:")
        self.select_button = QPushButton("Use this date")

        self.layout.addWidget(self.calendar)
        self.layout.addWidget(self.label)
        self.layout.addWidget(self.select_button)
        self.setLayout(self.layout)

        self.select_button.clicked.connect(self.return_date)
        self.calendar.selectionChanged.connect(self.update_label)

        self.selected_date = None
        self.update_label()

    def update_label(self):
        date = self.calendar.selectedDate()
        self.label.setText("Selected date: " + date.toString("yyyy-MM-dd"))

    def return_date(self):
        self.selected_date = self.calendar.selectedDate()
        self.close()

def get_date_from_calendar():
    app = QApplication(sys.argv)
    picker = CalendarPicker()
    picker.show()
    app.exec_()

    if picker.selected_date:
        return picker.selected_date.toPyDate() # Convert QDate to datetime.date
    return None

# For testing standalone
if __name__ == "__main__":
    picked = get_date_from_calendar()
    if picked:
        print("You picked:", picked)
    else:
        print("No date picked.")