from PyQt5.QtWidgets import QApplication
from GUI.BillingTrackerGUI import BillingTrackerGUI
import sys

def run_gui():
    app = QApplication(sys.argv)
    window = BillingTrackerGUI()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    run_gui()