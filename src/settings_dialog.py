from PyQt5.QtWidgets import (
        QDialog
)


class SettingsDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Settings")
        self.resize(300, 300)

        # Widgets I need:
        # Lunch duration : 
        # Daily Minutes Goal:
        



        
# Temporary for building the window 
if __name__ == "__main__":
    from PyQt5.QtWidgets import QApplication
    import sys
    app = QApplication(sys.argv)
    dlg = SettingsDialog()
    dlg.exec_()
