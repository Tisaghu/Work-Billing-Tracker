from PyQt5.QtWidgets import (
    QVBoxLayout, QHBoxLayout, 
    QLabel, QPushButton, QListWidget, 
    QLineEdit, QWidget
)

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

        # Minute chunks list
        self.chunk_list = QListWidget()

        # Bottom buttons
        self.add_button = QPushButton("Add")
        self.clear_button = QPushButton("Clear")
        self.done_button = QPushButton("Done")

        btn_layout = QHBoxLayout()
        btn_layout.addWidget(self.add_button)
        btn_layout.addWidget(self.clear_button)
        btn_layout.addWidget(self.done_button)

        self.layout.addWidget(QLabel("Enter time chunks (in minutes):"))
        self.layout.addWidget(self.minutes_input_field)
        self.layout.addWidget(self.description_input_field)
        self.layout.addWidget(self.chunk_list)
        self.layout.addLayout(btn_layout)
        self.setLayout(self.layout)

        # Connect buttons and input field
        self.add_button.clicked.connect(self.add_chunk)
        self.clear_button.clicked.connect(self.clear_chunks)
        self.on_done_callback = on_done_callback
        self.done_button.clicked.connect(self.done_clicked)
        self.minutes_input_field.returnPressed.connect(self.add_chunk)
        

    def add_chunk(self):
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

        self.minutes.append(minutes)
        self.chunk_list.addItem(f"{minutes} min")
        self.minutes_input_field.clear()

    def clear_chunks(self):
        self.minutes.clear()
        self.chunk_list.clear()

    def get_minutes(self):
        return self.minutes
    
    def done_clicked(self):
        if self.on_done_callback:
            self.on_done_callback(self.get_minutes(), self.description_input_field.text())
        self.clear_chunks() # Clear after adding