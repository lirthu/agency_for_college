import sys

from PyQt6.QtWidgets import QWidget, QApplication
from PyQt6.uic import loadUi


class ProfileWin(QWidget):
    def __init__(self):
        super().__init__()
        loadUi("ui/profile_menu.ui", self)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ProfileWin()
    window.show()
    sys.exit(app.exec())
