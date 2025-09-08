from PyQt5.QtWidgets import (
     QWidget, QVBoxLayout, QLabel, QFrame,
)

from PyQt5.QtGui import QFont

from PyQt5.QtCore import Qt

class StatsPanel(QWidget):
    def __init__(self):
        super().__init__()

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        # Create labels for each stat and store them for easy updates
        self.billed_today_title = QLabel("TODAY")
        self.billed_today_minutes_label = QLabel("Billed today: 0/0 min")
        self.billed_today_hours_label = QLabel("Billed today: 0/0 hours")
        self.today_percent_label = QLabel("Daily goal completion: 0%")

        self.billed_week_title = QLabel("WEEK")
        self.billed_week_minutes_label = QLabel("Billed this week: 0/0 min")
        self.billed_week_hours_label = QLabel("Billed this week: 0/0 hours")
        self.week_percent_label = QLabel("Weekly goal completion: 0%")

        self.billed_month_title = QLabel("MONTH")
        self.billed_month_minutes_label = QLabel("Billed this month: 0/0 min")
        self.billed_month_hours_label = QLabel("Billed this month: 0/0 hours")
        self.month_percent_label = QLabel("Monthly goal completion: 0%")

        self.goal_percent_label = QLabel("Weekly goal completion: 0%")
        self.minutes_remaining_label = QLabel("Minutes remaining: 0")

        # Fonts for title labels
        font = QFont()
        font.setBold(True)
        font.setPointSize(10)

        for lbl in [
            self.billed_today_title,
            self.billed_week_title,
            self.billed_month_title
        ]:
            lbl.setFont(font)

        # Create separators
        today_separator = QFrame()
        week_separator = QFrame()
        month_separator = QFrame()

        for seperator in [
            today_separator,
            week_separator,
            month_separator
        ]:
            seperator.setFrameShape(QFrame.HLine)
            seperator.setFrameShadow(QFrame.Sunken)

        # Make them look neat
        for lbl in [
            self.billed_today_title,
            self.billed_today_minutes_label,
            self.billed_today_hours_label,
            self.today_percent_label,
            today_separator,

            self.billed_week_title,
            self.billed_week_minutes_label,
            self.billed_week_hours_label,
            self.week_percent_label,
            week_separator,

            self.billed_month_title,
            self.billed_month_minutes_label,
            self.billed_month_hours_label,
            self.month_percent_label,
            month_separator,

            #self.goal_percent_label,
            self.minutes_remaining_label
        ]:
            #lbl.setAlignment(Qt.AlignLeft)
            self.layout.addWidget(lbl)

        self.layout.addStretch()  # Push everything up

    def update_stats(self, billed_today, billed_week, billed_month, today_goal, week_goal, month_goal):
        """
        Update stats dynamically from the main app.
        Shows billed/goal for today, week, and month.
        """
        # Update today labels
        self.billed_today_minutes_label.setText(f"Billed today: {billed_today}/{today_goal} min")
        self.billed_today_hours_label.setText(f"Billed today: {billed_today/60:.1f}/{today_goal/60} hours")
        self.today_percent_label.setText(f"Daily goal completion: {(billed_today/today_goal)*100:.1f}%")

        # Update week labels
        self.billed_week_minutes_label.setText(f"Billed this week: {billed_week}/{week_goal} min")
        self.billed_week_hours_label.setText(f"Billed this week: {billed_week/60:.1f}/{week_goal/60} hours")
        self.week_percent_label.setText(f"Weekly goal completion: {(billed_week/week_goal)*100:.1f}%")

        # Update month labels
        self.billed_month_minutes_label.setText(f"Billed this month: {billed_month}/{month_goal} min")
        self.billed_month_hours_label.setText(f"Billed this month: {billed_month/60:.1f}/{month_goal/60} hours")
        self.month_percent_label.setText(f"Monthly goal completion: {(billed_month/month_goal)*100:.1f}%")


        # Weekly percent and remaining
        if week_goal > 0:
            percent = (billed_week / week_goal) * 100
            remaining = week_goal - billed_week
        else:
            percent = 0
            remaining = 0
        self.goal_percent_label.setText(f"Weekly goal completion: {percent:.1f}%")
        self.minutes_remaining_label.setText(f"Minutes Remaining For This Week: {max(0, remaining)}")