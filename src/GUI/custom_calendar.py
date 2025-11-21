from PyQt5.QtWidgets import QCalendarWidget
from PyQt5.QtGui import QTextCharFormat, QColor
from PyQt5.QtCore import QDate, QTimer

class CustomCalendarWidget(QCalendarWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.apply_weekend_format(self.yearShown(), self.monthShown())
        self.setVerticalHeaderFormat(QCalendarWidget.NoVerticalHeader)
        self.currentPageChanged.connect(self.on_month_changed)
        self.highlight_today()
        self._last_highlighted_date = QDate.currentDate()
        self.start_refresh_timer()

    def on_month_changed(self, year, month):
        self.apply_weekend_format(year, month)
        self.highlight_today()

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

    def highlight_today(self):
        today_highlight_format = QTextCharFormat()
        today_highlight_format.setBackground(QColor("#F4F8A4"))
        today_highlight_format.setForeground(QColor("Black"))
        today = QDate.currentDate()
        self.setDateTextFormat(today, today_highlight_format)

    def _check_today_changed(self):
        """Called by the timer - if the system date rolled over, reapply formats."""
        now = QDate.currentDate()
        if now != getattr(self, "_last_highlighted_date", None):
            self.highlight_today()


    def start_refresh_timer(self):
        self._today_refresh_timer = QTimer(self)
        self._today_refresh_timer.setInterval(30* 60 * 1000) #Check every 30 minutes
        self._today_refresh_timer.timeout.connect(self._check_today_changed)
        self._today_refresh_timer.start()
        