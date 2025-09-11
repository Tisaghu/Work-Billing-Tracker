from PyQt5.QtWidgets import (
         QDialog, QSpinBox, QVBoxLayout, QHBoxLayout, QLabel
)

from PyQt5.QtCore import Qt

#Constants
MINUTES_LABEL_TEXT = "Min."
DAILY_GOAL_LABEL_TEXT = "Daily Goal Minutes:"
LUNCH_DURATION_LABEL_TEXT = "Lunch Duration:"


class SettingsDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Settings")
        self.resize(300, 300)

        self.dialog_layout = QVBoxLayout()
        self.setLayout(self.dialog_layout)

        #Daily minutes goal
        self.daily_goal_layout = QHBoxLayout()
        self.daily_goal_label = QLabel(DAILY_GOAL_LABEL_TEXT)
        self.daily_goal_box = QSpinBox()
        self.daily_goal_minutes_label = QLabel(MINUTES_LABEL_TEXT)

        self.daily_goal_layout.addWidget(self.daily_goal_label)
        self.daily_goal_layout.addWidget(self.daily_goal_box)
        self.daily_goal_layout.addWidget(self.daily_goal_minutes_label)


        #Lunch duration settings
        self.lunch_duration_layout = QHBoxLayout()
        self.lunch_duration_label = QLabel(LUNCH_DURATION_LABEL_TEXT)
        self.lunch_duration_box = QSpinBox()
        self.lunch_duration_minutes_label = QLabel(MINUTES_LABEL_TEXT)

        self.lunch_duration_layout.addWidget(self.lunch_duration_label)
        self.lunch_duration_layout.addWidget(self.lunch_duration_box)
        self.lunch_duration_layout.addWidget(self.lunch_duration_minutes_label)


        #Add layouts to the main dialog layout
        self.dialog_layout.setAlignment(Qt.AlignTop)
        self.dialog_layout.addLayout(self.daily_goal_layout)
        self.dialog_layout.addLayout(self.lunch_duration_layout)
        

    


        
# Temporary for building the window 
if __name__ == "__main__":
    from PyQt5.QtWidgets import QApplication
    import sys
    app = QApplication(sys.argv)
    dlg = SettingsDialog()
    dlg.exec_()
