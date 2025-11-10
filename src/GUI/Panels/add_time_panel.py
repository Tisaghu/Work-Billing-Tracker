from PyQt5.QtWidgets import (
    QVBoxLayout, QHBoxLayout, 
    QLabel, QPushButton, QListWidget, 
    QLineEdit, QWidget, 
)

from PyQt5.QtGui import QFont

class AddTimePanel(QWidget):
    """
    Panel in the main gui for adding chunks of worked time along with a description.
    """
    def __init__(self, on_done_callback=None):
        super().__init__()
        self.setWindowTitle("Add Time Chunks")
        self.resize(300, 300)

        self.minutes = []

        self.layout = QVBoxLayout()

        # Minutes input field
        self.minutes_input_field = QLineEdit()
        self.minutes_input_field.setPlaceholderText("Enter minutes and press Add or Enter")

        # Description input field
        self.description_input_field = QLineEdit()
        self.description_input_field.setPlaceholderText("(Optional Description)")

        # Bottom buttons
        self.add_button = QPushButton("Add")
        self.clear_button = QPushButton("Clear")
        self.done_button = QPushButton("Done")

        btn_layout = QHBoxLayout()
        btn_layout.addWidget(self.done_button)

        # Font for main label to make it stand out
        LargeBoldFont = QFont()
        LargeBoldFont.setBold(True)
        LargeBoldFont.setPointSize(10)
        Add_Time_Main_Label = QLabel("Enter time chunks (in minutes):")
        Add_Time_Main_Label.setFont(LargeBoldFont)

        self.layout.addWidget(Add_Time_Main_Label)
        self.layout.addWidget(self.minutes_input_field)
        self.layout.addWidget(self.description_input_field)
        self.layout.addLayout(btn_layout)
        self.setLayout(self.layout)

        # Connect buttons and input field
        self.on_done_callback = on_done_callback
        self.done_button.clicked.connect(self.done_clicked)
        self.minutes_input_field.returnPressed.connect(self.done_clicked)
        

    def get_minutes(self):
        return self.minutes
    
    def done_clicked(self):
        text = self.minutes_input_field.text().strip()
        if not text:
            return
        try:
            minutes = int(text)
            if minutes <= 0:
                raise ValueError
        except ValueError:
            self.minutes_input_field.setText("")
            self.minutes_input_field.setPlaceholderText("Invalid! Enter a positive number")
            return
        if self.on_done_callback:
            self.on_done_callback(minutes, self.description_input_field.text())
            self.minutes_input_field.clear()