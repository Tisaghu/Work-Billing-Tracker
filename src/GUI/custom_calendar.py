from PyQt5.QtWidgets import QCalendarWidget
from PyQt5.QtGui import QTextCharFormat, QColor
from PyQt5.QtCore import QDate, Qt

class CustomCalendarWidget(QCalendarWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.apply_weekend_format(self.yearShown(), self.monthShown())
        self.setVerticalHeaderFormat(QCalendarWidget.NoVerticalHeader)
        self.currentPageChanged.connect(self.on_month_changed)

    def on_month_changed(self, year, month):
        self.apply_weekend_format(year, month)

    def apply_weekend_format(self, year, month):
        # Helper functions
        def prev_month_year(month, year):
            return (month - 1 if month > 1 else 12, year if month > 1 else year - 1)
        def next_month_year(month, year):
            return (month + 1 if month < 12 else 1, year if month < 12 else year + 1)

        months = [
            prev_month_year(month, year),
            (month, year),
            next_month_year(month, year)
        ]

        # Clear all formatting first
        clear_format = QTextCharFormat()
        for m, y in months:
            first_day = QDate(y, m, 1)
            last_day = QDate(y, m, first_day.daysInMonth())
            for day in range(1, last_day.day() + 1):
                qdate = QDate(y, m, day)
                self.setDateTextFormat(qdate, clear_format)

        # Apply dark gray to weekends
        dark_gray_format = QTextCharFormat()
        dark_gray_format.setBackground(QColor("#444444"))
        dark_gray_format.setForeground(QColor("white"))
        for m, y in months:
            first_day = QDate(y, m, 1)
            last_day = QDate(y, m, first_day.daysInMonth())
            for day in range(1, last_day.day() + 1):
                qdate = QDate(y, m, day)
                if qdate.dayOfWeek() in (6, 7):
                    self.setDateTextFormat(qdate, dark_gray_format)