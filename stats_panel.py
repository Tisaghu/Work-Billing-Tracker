from PyQt5.QtWidgets import (
     QWidget, QVBoxLayout, QLabel, 
)

from PyQt5.QtCore import Qt

class StatsPanel(QWidget):
    def __init__(self):
        super().__init__()

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        # Create labels for each stat and store them for easy updates
        self.billed_today_label = QLabel("Billed today: 0/0 min")
        self.billed_week_label = QLabel("Billed this week: 0/0 min")
        self.billed_month_label = QLabel("Billed this month: 0/0 min")
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

    def update_stats(self, billed_today, billed_week, billed_month, today_goal, week_goal, month_goal):
        """
        Update stats dynamically from your main app.
        Shows billed/goal for today, week, and month.
        """
        self.billed_today_label.setText(f"Billed today: {billed_today}/{today_goal} min")
        self.billed_week_label.setText(f"Billed this week: {billed_week}/{week_goal} min")
        self.billed_month_label.setText(f"Billed this month: {billed_month}/{month_goal} min")

        # Weekly percent and remaining
        if week_goal > 0:
            percent = (billed_week / week_goal) * 100
            remaining = week_goal - billed_week
        else:
            percent = 0
            remaining = 0
        self.goal_percent_label.setText(f"Weekly goal completion: {percent:.1f}%")
        self.minutes_remaining_label.setText(f"Minutes Remaining For This Week: {max(0, remaining)}")